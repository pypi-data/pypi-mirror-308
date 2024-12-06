import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
import spyctl.api.athena_search as search_api

from app.reports.reporter import Reporter
import app.reports.mdx_lib as mdx_lib

logger = logging.getLogger("uvicorn")


class CUPSReporter(Reporter):

    def __init__(self, spec: dict):
        super().__init__(spec)
        self.error = {}
        self.context = {}
        self.impacted_processes = []
        self.impacted_machines = []

    def collect_and_process(
        self,
        args: dict[str, str | float | int | bool],
        org_uid: str,
        api_key: str,
        api_url: str,
    ) -> None:

        end_time = int(args["time"])
        start_time = end_time - 60 * 60 * 2

        logger.info(
            "cups report: Starting collection and processing of processes and machines"
        )

        query = f'exe ~= "*cups-browsed*"'

        self.context["time"] = end_time
        self.context["impacted_procs"] = search_api.search_athena(
            api_url,
            api_key,
            org_uid,
            schema="model_process",
            query=query,
            start_time=start_time,
            end_time=end_time,
            use_pbar=False,
        )

        if len(self.context["impacted_procs"]) == 0:
            return

        muids = [proc["muid"] for proc in self.context["impacted_procs"]]
        query = f'id="{muids[0]}"'
        if len(muids) > 1:
            for muid in muids[1:]:
                query += f' or id="{muid}"'
        self.context["impacted_machines"] = search_api.search_athena(
            api_url,
            api_key,
            org_uid,
            schema="model_machine",
            query=query,
            start_time=start_time,
            end_time=end_time,
            use_pbar=False,
        )

    def renderer(
        self,
        fmt: str,
        rid: str,
    ) -> Path:
        if self.error:
            return self.render(self.error, fmt, rid)

        # For MDX format, we need to convert this to grid definitions to render
        if fmt == "mdx":
            # Export dataframes to mdx context
            mdx_context = self.make_mdx_context(self.context)
            return self.render(mdx_context, fmt, rid)
        else:
            return super().renderer(fmt, rid)

    def make_mdx_context(self, context: dict) -> dict:
        if "error" in context:
            return context

        mdx_context = {}
        mdx_context["time"] = datetime.fromtimestamp(
            context["time"], timezone.utc
        ).strftime("%Y-%m-%d %H:%M:%S %Z")

        if len(self.context["impacted_procs"]) == 0:
            mdx_context["impacted"] = False
            return mdx_context

        mdx_context["impacted"] = True
        mdx_context["impacted_procs_grid"] = mdx_lib.make_grid(
            columns=[
                {"title": "PID", "field": "pid"},
                {"title": "Executable", "field": "exe"},
                {"title": "Cgroup", "field": "cgroup"},
                {"title": "Machine UID", "field": "muid"},
            ],
            data=self.context["impacted_procs"],
        )

        mdx_context["impacted_machines_grid"] = mdx_lib.make_grid(
            columns=[
                {"title": "Hostname", "field": "hostname"},
                {"title": "Public IP", "field": "public_ip"},
                {"title": "Description", "field": "description"},
            ],
            data=self.context["impacted_machines"],
        )

        return mdx_context
