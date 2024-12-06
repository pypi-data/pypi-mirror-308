from datetime import datetime, timezone
from pathlib import Path
import json
import spyctl.api.athena_search as search_api
import pandas as pd
from app.reports.reporter import Reporter, _basedir
import app.reports.mdx_lib as mdx_lib

s_org = "model_organization"


class AWSReporter(Reporter):

    def __init__(self, spec: dict):
        super().__init__(spec)
        self.error = {}
        self.context = {}
        self.cluster_summary = pd.DataFrame()
        self.instance_summary = pd.DataFrame()

    def collect_and_process(
        self,
        args: dict[str, str | float | int | bool],
        org_uid: str,
        api_key: str,
        api_url: str,
    ):
        time = int(args["time"])
        self.context["time"] = time

        # Get the organization data
        src = f"org:{org_uid}"
        data = search_api.search_athena(
            api_url,
            api_key,
            org_uid,
            schema="model_organization",
            query=f'id="{src}"',
            start_time=time - 3600,
            end_time=time,
            use_pbar=False,
            quiet=True,
        )

        if not data:
            self.error = {
                "error": {
                    "message": "It looks like there is currently no AWS data available. This could mean that there is no AWS agent deployed yet to pull your AWS Account information into the Spyderbat backend"
                }
            }
            return

        model_org = data[0]

        # Analyze the EKS clusters
        df_eks_clusters = pd.DataFrame(model_org["EksClusters"])
        df_eks_clusters["monitored"] = ~df_eks_clusters["cluster_uid"].isna()
        df_eks_clusters["monitored"] = df_eks_clusters["monitored"].apply(
            lambda x: "Yes" if x else "No"
        )
        drop_cols = [
            "expire_at",
            "valid_from",
            "version",
            "schema",
            "time",
            "aws_account_uid",
            "kind",
            "arn",
        ]
        df_eks_clusters.drop(columns=drop_cols, inplace=True)
        df_eks_clusters["node_group"] = df_eks_clusters["node_groups"].apply(
            lambda x: [v for v in x.values()]
        )
        df_eks_nodegroups = df_eks_clusters.explode("node_group").reset_index(
            drop=True
        )
        df_eks_nodegroups.drop(columns=["node_groups"], inplace=True)
        meta = pd.json_normalize(df_eks_nodegroups["cluster_meta"])
        meta.rename(columns={"status": "cluster_status"}, inplace=True)
        nodegroup_info = pd.json_normalize(df_eks_nodegroups["node_group"])
        nodegroup_info.rename(
            columns={"status": "nodegroup_status"}, inplace=True
        )
        df_eks_nodegroups = pd.concat(
            [df_eks_nodegroups, meta, nodegroup_info], axis=1
        )
        df_eks_nodegroups.drop(
            columns=["cluster_meta", "node_group"], inplace=True
        )
        df_eks_nodegroups["instanceTypes"] = df_eks_nodegroups[
            "instanceTypes"
        ].apply(lambda x: x[0] if len(x) == 1 else ", ".join(x))

        columns = [
            "aws_account_id",
            "region",
            "monitored",
            "name",
            "version",
            "cluster_status",
        ]
        mask = df_eks_nodegroups.status == "active"
        self.cluster_monitored = df_eks_clusters.groupby("monitored").count()
        self.cluster_summary = (
            df_eks_nodegroups[mask]
            .groupby(columns)
            .agg(
                {
                    "nodegroupName": "count",
                    "scalingConfig.minSize": "count",
                    "scalingConfig.maxSize": "count",
                    "scalingConfig.desiredSize": "count",
                    "instanceTypes": "unique",
                    "amiType": "unique",
                }
            )
            .rename(
                columns={
                    "nodegroupName": "Nr Nodegroups",
                    "scalingConfig.minSize": "Min Nodes",
                    "scalingConfig.maxSize": "Max Nodes",
                    "scalingConfig.desiredSize": "Desired Nodes",
                    "instanceTypes": "Instance Types",
                    "amiType": "AMI Types",
                }
            )
        )
        self.cluster_summary["Instance Types"] = self.cluster_summary[
            "Instance Types"
        ].apply(lambda x: x[0] if len(x) == 1 else ", ".join(x))
        self.cluster_summary["AMI Types"] = self.cluster_summary[
            "AMI Types"
        ].apply(lambda x: x[0] if len(x) == 1 else ", ".join(x))

        # Analyze the EC2 instances
        df_instances = pd.DataFrame(model_org["Ec2Instances"])
        df_instances["monitored"] = ~df_instances["muid"].isna()
        df_instances["monitored"] = df_instances["monitored"].apply(
            lambda x: "Yes" if x else "No"
        )
        drop_cols = [
            "expire_at",
            "valid_from",
            "version",
            "schema",
            "time",
            "aws_account_uid",
            "kind",
        ]
        df_instances.drop(columns=drop_cols, inplace=True)
        cpu_options = pd.json_normalize(df_instances["CpuOptions"])
        df_instances = pd.concat([df_instances, cpu_options], axis=1)
        df_instances.drop(columns=["CpuOptions"], inplace=True)


        columns = [
            "aws_account_id",
            "region",
            "monitored",
            "name",
            "instance_id",
            "InstanceType",
            "CoreCount",
            "Architecture",
        ]
        self.instance_summary = df_instances[columns].groupby(columns).count()
        self.instances_monitored = self.instance_summary.groupby(
            "monitored"
        ).count()

        # Make a coverage summary
        inst_sum = df_instances.groupby(
            ["aws_account_id", "monitored"]
        ).count()["id"]
        eks_sum = df_eks_clusters.groupby(
            ["aws_account_id", "monitored"]
        ).count()["id"]
        combined = pd.concat(
            [inst_sum, eks_sum], axis=0, keys=["EC2 Instances", "EKS Clusters"]
        )
        df = combined.reset_index().rename(
            columns={"level_0": "Resource Type", "id": "Count"}
        )
        coverage = (
            df.groupby(["aws_account_id", "Resource Type", "monitored"])
            .sum()
            .unstack()
            .fillna(0)
        )
        coverage.columns = coverage.columns.droplevel()
        coverage["Total"] = coverage["No"] + coverage["Yes"]
        coverage["Coverage"] = coverage["Yes"] / coverage["Total"]
        coverage["Coverage"] = coverage["Coverage"].apply(
            lambda x: "{:.0%}".format(x)
        )
        coverage.reset_index(inplace=True)
        coverage = coverage[
            ["aws_account_id", "Resource Type", "Total", "Yes", "Coverage"]
        ]
        coverage.rename(
            columns={
                "aws_account_id": "AWS Account ID",
                "Yes": "Monitored",
                "Monitoring Coverage": "Coverage",
            },
            inplace=True,
        )
        self.coverage = coverage

        self.context.update(
            {
                "cluster_summary": json.loads(
                    self.cluster_summary.reset_index().to_json(
                        orient="records"
                    )
                ),
                "instance_summary": json.loads(
                    self.instance_summary.reset_index().to_json(
                        orient="records"
                    )
                ),
                "coverage": json.loads(
                    self.coverage.to_json(orient="records")
                ),
            }
        )

    def renderer(self, fmt: str, rid: str) -> Path:

        if self.error:
            return self.render(self.error, fmt, rid)

        if fmt == "mdx":
            mdx_context = self.make_mdx_context(self.context)
            return self.render(mdx_context, fmt, rid)
        if fmt == "xlsx":
            # Create a Pandas Excel writer using XlsxWriter as the engine
            outfile = Path(_basedir) / Path(f"{rid}.xlsx")
            with pd.ExcelWriter(outfile, engine="xlsxwriter") as writer:
                # Write each DataFrame to a different worksheet
                self.coverage.to_excel(
                    writer, sheet_name="Coverage Summary", index=False
                )
                self.cluster_summary.to_excel(
                    writer, sheet_name="EKS Clusters"
                )
                self.instance_summary.to_excel(
                    writer, sheet_name="EC2 Instances"
                )
            return outfile

        else:
            return super().renderer(fmt, rid)

    def make_mdx_context(self, context: dict) -> dict:

        mdx_ctx = {}
        mdx_ctx["time"] = (
            datetime.fromtimestamp(context["time"], timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S %Z"
            ),
        )
        mdx_ctx["coverage_grid"] = mdx_lib.make_grid_df(
            self.coverage, grid_options={"rowspanning": True}
        )

        mdx_ctx["cluster_summary_grid"] = mdx_lib.make_grid_df(
            self.cluster_summary.reset_index(),
            grid_options={"rowspanning": True},
        )

        mdx_ctx["instance_summary_grid"] = mdx_lib.make_grid_df(
            self.instance_summary.reset_index(),
            grid_options={"rowspanning": True},
        )

        return mdx_ctx
