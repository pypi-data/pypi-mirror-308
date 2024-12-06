from datetime import datetime, timezone
from pathlib import Path
import json
import spyctl.api.athena_search as search_api
import pandas as pd
from app.reports.reporter import Reporter, _basedir
import app.reports.mdx_lib as mdx_lib

s_org = "model_organization"


def summarize_k8s_rules(rules: list) -> list:
    if isinstance(rules, float):
        return [""]
    return [summarize_k8s_rule(rule) for rule in rules]


def summarize_k8s_rule(rule: dict) -> str:
    api_groups = group_to_str(rule.get("apiGroups", []))
    resources = group_to_str(rule.get("resources", []))
    verbs = group_to_str(rule.get("verbs", []))
    rv = ""
    if api_groups:
        rv += f"{api_groups} -"
    if verbs:
        rv += f" {verbs} -"
    if resources:
        rv += f" {resources}"

    return rv


def group_to_str(group: list) -> str:
    rv = ""
    if not group:
        return ""
    if isinstance(group, str):
        return group
    if len(group) == 1:
        return group[0]
    for g in group[:-1]:
        if g:
            rv += f"{g}, "
    if group[-1]:
        rv += f"{group[-1]}"
    return rv


def summarize_attached_policies(policies: list) -> list:
    if isinstance(policies, float):
        return [""]
    return [
        summarize_statement(statement)
        for policy in policies
        for statement in get_attached_policy_statements(policy)
    ]


def get_attached_policy_statements(policy: dict) -> list:
    return (
        policy.get("default_version", {})
        .get("policy", {})
        .get("Document", {})
        .get("Statement", [])
    )


def summarize_inline_policies(policies: list) -> list:
    if isinstance(policies, float):
        return [""]
    return [
        summarize_statement(statement)
        for policy in policies
        for statement in policy.get("Statement", [])
    ]


def summarize_aws_policies(row) -> list:
    inline_summary = summarize_inline_policies(
        row.get("aws_inline_policies", [])
    )
    attached_summary = summarize_attached_policies(
        row.get("aws_attached_policies", [])
    )
    if not inline_summary:
        return attached_summary
    if not attached_summary:
        return inline_summary
    return inline_summary + attached_summary


def summarize_statement(statement: dict) -> str:
    effect = statement.get("Effect", "")
    actions = group_to_str(statement.get("Action", []))
    resources = group_to_str(statement.get("Resource", []))
    return f"{effect} - {actions} on: {resources}"


class RbacReporter(Reporter):

    def __init__(self, spec: dict):
        super().__init__(spec)
        self.error = {}
        self.context = {}

    def collect_and_process(
        self,
        args: dict[str, str | float | int | bool],
        org_uid: str,
        api_key: str,
        api_url: str,
    ):
        end = time = int(args["time"])
        start = time - 7200
        self.context["time"] = time

        cluid = args.get("cluid")

        k8s_data = []
        cluster = search_api.search_athena(
            api_url,
            api_key,
            org_uid,
            schema="model_k8s_cluster",
            query=f'id="{cluid}"',
            start_time=start,
            end_time=end,
            use_pbar=False,
            quiet=True,
        )

        k8s_data += cluster

        for schema in [
            "model_k8s_role",
            "model_k8s_rolebinding",
            "model_k8s_clusterrole",
            "model_k8s_clusterrolebinding",
            "model_k8s_serviceaccount",
            "model_k8s_deployment",
            "model_k8s_daemonset",
            "model_k8s_statefulset",
        ]:
            data = search_api.search_athena(
                api_url,
                api_key,
                org_uid,
                schema=schema,
                query=f'cluster_uid="{cluid}"',
                start_time=start,
                end_time=end,
                use_pbar=False,
                quiet=True,
            )
            k8s_data += data

        df = pd.DataFrame(k8s_data)

        if df.empty:
            self.error = {
                "error": {
                    "message": "It looks like there is currently no Kubernetes data available for this cluster for the selected time."
                }
            }
            return

        # Get the cluster model to get the cluster name
        cluster_name = ""
        clusters = df[df.kind == "Cluster"]
        if not clusters.empty:
            cluster_name = clusters.name.iloc[0]
        self.context["cluster_name"] = cluster_name

        # Process the kubernetes data

        # Extract service account, name and namespace as separate columns
        df["service_account"] = pd.json_normalize(df.spec)[
            "template.spec.serviceAccount"
        ]
        df[["name", "namespace"]] = pd.json_normalize(df.metadata)[
            ["name", "namespace"]
        ]

        # Extract all roles, service accounts and role bindings in separate dataframes for joining

        # Service accounts first
        serviceAccounts = (
            df[df.kind == "ServiceAccount"].reset_index(drop=True).copy()
        )
        svc_acc_cols = [
            "name",
            "namespace",
            "kind",
            "metadata",
            "aws_role_arn",
            "aws_role_uid",
        ]
        if "aws_role_arn" not in serviceAccounts.columns:
            serviceAccounts["aws_role_arn"] = ""
        if "aws_role_uid" not in serviceAccounts.columns:
            serviceAccounts["aws_role_uid"] = ""

        # Kubernetes roles and cluster roles
        roles = (
            df[(df.kind == "Role") | (df.kind == "ClusterRole")]
            .reset_index(drop=True)
            .copy()
        )
        role_cols = ["kind", "name", "namespace", "rules"]

        # Find any service accounts with associated AWS IAM roles and make list of all aws account ids
        iam_cols = [
            "arn",
            "RoleName",
            "AssumeRolePolicyDocument",
            "inline_policies",
            "attached_role_policies",
        ]
        iam_roles = pd.DataFrame(columns=iam_cols)

        if "aws_account_id" in serviceAccounts.columns:
            aws_accounts = serviceAccounts.aws_account_id.dropna().unique()

            # See if we can pull the IAM roles for that account (if an aws agent is pulling that info)

            iam_roles = pd.DataFrame()
            for account_id in aws_accounts:
                aws_data = search_api.search_athena(
                    api_url=api_url,
                    api_key=api_key,
                    org_uid=org_uid,
                    schema="model_aws_iam_role",
                    query=f'aws_account_id="{account_id}"',
                    start_time=start,
                    end_time=end,
                    use_pbar=False,
                    quiet=True,
                )
                iam_roles = pd.concat([iam_roles, pd.DataFrame(aws_data)])

            if not iam_roles.empty:
                iam_roles = iam_roles[iam_cols].reset_index(drop=True).copy()

        # Get the role bindings - which provide the many to many mapping between roles and service accounts
        bindings = (
            df[(df.kind == "RoleBinding") | (df.kind == "ClusterRoleBinding")]
            .reset_index(drop=True)
            .copy()
        )
        # Need to explode bindings cause they can reference multiple subjects.
        bindings = bindings.explode("subjects").reset_index(drop=True)

        # then get only required subject and roleRef fields
        bindings[["roleRefKind", "roleRefName"]] = pd.json_normalize(
            bindings["roleRef"]
        )[["kind", "name"]]
        bindings[
            [
                "subjectApiGroup",
                "subjectKind",
                "subjectName",
                "subjectNamespace",
            ]
        ] = pd.json_normalize(bindings["subjects"])[
            ["apiGroup", "kind", "name", "namespace"]
        ]
        binding_cols = [
            "roleRefKind",
            "roleRefName",
            "subjectKind",
            "subjectName",
            "subjectNamespace",
        ]

        # Now we can join it all up to get full picture

        # Merge bindings to roles
        merged1 = pd.merge(
            left=bindings[binding_cols],
            right=roles[role_cols],
            left_on=["roleRefKind", "roleRefName"],
            right_on=["kind", "name"],
            how="left",
        )
        merged1.drop(columns=["kind", "name", "namespace"], inplace=True)

        # Merge bindings to service accounts
        merged2 = pd.merge(
            left=merged1,
            right=serviceAccounts[svc_acc_cols],
            left_on=["subjectKind", "subjectName", "subjectNamespace"],
            right_on=["kind", "name", "namespace"],
            how="right",
        )

        # account_to_k8s maps a service account to its associated roles and
        # their rbac rules
        account_to_k8srules = merged2[
            [
                "kind",
                "name",
                "namespace",
                "aws_role_arn",
                "aws_role_uid",
                "roleRefName",
                "rules",
            ]
        ].copy()
        account_to_k8srules.rename(
            columns={"roleRefName": "roleName"}, inplace=True
        )

        # Now merge in with the IAM roles, if we have any
        account_to_rules = pd.merge(
            left=account_to_k8srules,
            right=iam_roles,
            left_on="aws_role_arn",
            right_on="arn",
            how="left",
        )
        account_to_rules.rename(
            columns={
                "kind": "svc_account_kind",
                "name": "svc_account_name",
                "namespace": "svc_account_namespace",
                "RoleName": "aws_role_name",
                "AssumeRolePolicyDocument": "aws_assume_role_policy",
                "inline_policies": "aws_inline_policies",
                "attached_role_policies": "aws_attached_policies",
            },
            inplace=True,
        )

        # Summarize the rbac rules and permissions
        account_to_rules["rules_summary"] = account_to_rules.rules.apply(
            lambda x: summarize_k8s_rules(x)
        )
        account_to_rules["aws_permissions"] = account_to_rules.apply(
            summarize_aws_policies, axis=1
        )

        # Merge the resources with service accounts to the service account rbac summary
        resources = (
            df[df.service_account.notnull()].reset_index(drop=True).copy()
        )
        res_cols = ["kind", "name", "namespace", "service_account"]
        rules_cols = [
            "svc_account_kind",
            "svc_account_namespace",
            "svc_account_name",
            "roleName",
            "rules_summary",
            "aws_role_arn",
            "aws_role_name",
            "aws_assume_role_policy",
            "aws_permissions",
        ]
        df_rbac = pd.merge(
            left=resources[res_cols],
            right=account_to_rules[rules_cols],
            left_on=["service_account", "namespace"],
            right_on=["svc_account_name", "svc_account_namespace"],
            how="left",
        )

        df_rbac.rename(
            columns={"rules_summary": "k8s rbac permissions"}, inplace=True
        )
        df_rbac[
            [
                "roleName",
                "aws_role_arn",
                "aws_role_name",
                "aws_assume_role_policy",
            ]
        ] = df_rbac[
            [
                "roleName",
                "aws_role_arn",
                "aws_role_name",
                "aws_assume_role_policy",
            ]
        ].fillna(
            ""
        )

        self.rbac_analysis = df_rbac

        self.context.update(
            {
                "rbac_analysis": self.rbac_analysis,
            }
        )

    def renderer(self, fmt: str, rid: str) -> Path:

        if self.error:
            return self.render(self.error, fmt, rid)

        if fmt == "mdx":
            mdx_context = self.make_mdx_context(self.context)
            return self.render(mdx_context, fmt, rid)
        if fmt == "xlsx":
            # Remove time and cluster name from context
            # so the excel writer doesn't try to make these into
            # separate sheets
            xlsx_context = {"rbac_analysis": self.rbac_analysis}
            return self.render(xlsx_context, fmt, rid)
        else:
            return super().renderer(fmt, rid)

    def make_mdx_context(self, context: dict) -> dict:

        mdx_ctx = {}
        mdx_ctx["cluster_name"] = context["cluster_name"]
        mdx_ctx["time"] = (
            datetime.fromtimestamp(context["time"], timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S %Z"
            ),
        )

        k8s_data_cols = ["roleName", "k8s rbac permissions"]
        k8s_rename_cols = ["Role Name", "Role Permissions"]
        k8s_perms = k8s_rename_cols[-1]

        aws_data_cols = ["aws_role_name", "aws_permissions"]
        aws_rename_cols = [
            "Associated IAM Role",
            "AWS Role Permissions",
        ]
        aws_perms = aws_rename_cols[-1]

        mdx_ctx["resources"] = []
        for namespace, namespace_data in self.rbac_analysis.groupby(
            "namespace"
        ):
            ns_data = []
            for kind_name_acct, data in namespace_data.groupby(
                ["kind", "name", "service_account"]
            ):
                rv = dict()
                rv["kind"], rv["name"], rv["service_account"] = kind_name_acct
                rv["has_k8s_role"] = not data[data.roleName != ""].empty
                aws_data = data[data.aws_role_name != ""][aws_data_cols]
                rv["has_aws_role"] = not aws_data.empty

                if rv["has_k8s_role"]:
                    k8s_data = data[k8s_data_cols].rename(
                        columns=dict(zip(k8s_data_cols, k8s_rename_cols))
                    )
                    k8s_data = k8s_data.explode(k8s_perms)
                    rv["k8s_rbac_grid"] = mdx_lib.make_grid_df(
                        k8s_data,
                        grid_options={
                            "rowspanning": True,
                            "autoRowHeight": True,
                        },
                    )
                if rv["has_aws_role"]:
                    aws_data = aws_data.rename(
                        columns=dict(zip(aws_data_cols, aws_rename_cols))
                    )
                    aws_data = aws_data.explode(aws_perms)
                    rv["aws_rbac_grid"] = mdx_lib.make_grid_df(
                        aws_data,
                        grid_options={
                            "rowspanning": True,
                            "autoRowHeight": True,
                        },
                    )
                ns_data.append(rv)
            mdx_ctx["resources"].append(
                {"namespace": namespace, "data": ns_data}
            )

        return mdx_ctx
