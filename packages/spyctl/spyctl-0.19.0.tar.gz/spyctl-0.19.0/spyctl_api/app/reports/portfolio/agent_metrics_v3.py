import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from copy import deepcopy

import pandas as pd
import spyctl.resources.api_filters as _af
from spyctl.api.agents import get_agents
from spyctl.api.source_queries import retrieve_data

from app.reports.reporter import Reporter
import app.reports.mdx_lib as mdx_lib


_METRIC_KEYS = [
    "ref",
    "time",
    "mem_1min_B",
    "cpu_1min_P",
    "bandwidth_1min_Bps",
]

logger = logging.getLogger("uvicorn")


def metric_project(metric: dict) -> dict:
    return {k: metric[k] for k in _METRIC_KEYS}


class AgentMetricsReporter(Reporter):

    def __init__(self, spec: dict):
        super().__init__(spec)
        self.agents = []
        self.df = pd.DataFrame()
        self.error = {}
        self.context = {}

    def collect_and_process(
        self,
        args: dict[str, str | float | int | bool],
        org_uid: str,
        api_key: str,
        api_url: str,
    ) -> None:

        start_time = int(args["st"])
        now = time.time()
        if now - start_time < 60 * 60 * 2:
            start_time = now - 60 * 60 * 2
        end_time = int(args["et"])

        sources = [f"global:{org_uid}"]
        filters = {"cluster": args["cluster"]}
        pipeline = _af.Agents.generate_pipeline(
            None, None, True, filters=filters
        )

        # Get the list of agents present in the reporting period
        self.agents = list(
            get_agents(
                api_url,
                api_key,
                org_uid,
                sources,
                time=(start_time, end_time),
                pipeline=pipeline,
                limit_mem=False,
                disable_pbar=True,
            )
        )

        sources = [agent["muid"] for agent in self.agents]

        # Collect and process the metrics by time slice of a day
        st = start_time
        et = min(end_time, st + 60 * 60 * 12)

        logger.info(
            "agent_metrics: Starting collection and processing of agent metrics"
        )
        while st < end_time:
            metrics = self.get_metrics(
                st, et, sources, org_uid, api_key, api_url
            )
            self.update_df(metrics)
            progress = (et - start_time) / (end_time - start_time)
            logger.info(f"agent_metrics: Collection progress: {progress:.2%}")

            st = et
            et = min(end_time, st + 60 * 60 * 12)

        if len(self.df) == 0:
            self.error = {"error": {"message": "No data available"}}
            return

        # Join with agents to get the agent hostname
        agents = pd.DataFrame(self.agents)[["id", "hostname"]]
        self.df = self.df.merge(agents, left_on="ref", right_on="id")

        # Calculate the metrics
        self.metrics_by_agent_mean = self.df.groupby(["hostname", "id"])[
            ["cpu", "mem", "network"]
        ].mean()
        self.metrics_by_agent_p90 = self.df.groupby(["hostname", "id"])[
            ["cpu", "mem", "network"]
        ].quantile(0.90)
        self.metrics_by_agent_p99 = self.df.groupby(["hostname", "id"])[
            ["cpu", "mem", "network"]
        ].quantile(0.99)

        self.metrics_mean = self.df[["cpu", "mem", "network"]].mean()
        self.metrics_p90 = self.df[["cpu", "mem", "network"]].quantile(0.90)
        self.metrics_p99 = self.df[["cpu", "mem", "network"]].quantile(0.99)

        # Fill out the rest of the context
        # Cluster name
        self.context["cluster"] = {
            "name": args["cluster"],
        }

        self.context["st"] = int(args["st"])
        self.context["et"] = int(args["et"])

        # Export frames to dicts context
        self.context["metrics_summary"] = {
            "cpu": {
                "mean": self.metrics_mean["cpu"],
                "p90": self.metrics_p90["cpu"],
                "p99": self.metrics_p99["cpu"],
            },
            "mem": {
                "mean": self.metrics_mean["mem"],
                "p90": self.metrics_p90["mem"],
                "p99": self.metrics_p99["mem"],
            },
            "bps": {
                "mean": self.metrics_mean["network"],
                "p90": self.metrics_p90["network"],
                "p99": self.metrics_p99["network"],
            },
        }

        self.context["agent_metrics"] = {}

        def update_metric(out_metrics, input_metric, mtype):
            for rec in input_metric:
                out_metrics.setdefault(rec["id"], {})
                out_metrics[rec["id"]]["name"] = rec["hostname"]
                out_metrics[rec["id"]].setdefault("cpu", {})
                out_metrics[rec["id"]]["cpu"][mtype] = rec["cpu"]
                out_metrics[rec["id"]].setdefault("mem", {})
                out_metrics[rec["id"]]["mem"][mtype] = rec["mem"]
                out_metrics[rec["id"]].setdefault("bps", {})
                out_metrics[rec["id"]]["bps"][mtype] = rec["network"]

        update_metric(
            self.context["agent_metrics"],
            self.metrics_by_agent_mean.reset_index().to_dict(
                orient="records"
            ),
            "mean",
        )
        update_metric(
            self.context["agent_metrics"],
            self.metrics_by_agent_p90.reset_index().to_dict(
                orient="records"
            ),
            "p90",
        )
        update_metric(
            self.context["agent_metrics"],
            self.metrics_by_agent_p99.reset_index().to_dict(
                orient="records"
            ),
            "p99",
        )

    def update_df(self, metrics: Iterable) -> None:
        df_metrics = pd.DataFrame(metrics)
        if len(df_metrics) == 0:
            return
        mem = pd.json_normalize(df_metrics.mem_1min_B).fillna(0)["agent"]
        cpu = pd.json_normalize(df_metrics.cpu_1min_P).fillna(0)["agent"]
        df_metrics["mem"] = mem
        df_metrics["cpu"] = cpu
        df_metrics.rename(
            columns={"bandwidth_1min_Bps": "network"}, inplace=True
        )
        df_selection = df_metrics[["ref", "time", "mem", "cpu", "network"]]
        if self.df.empty:
            self.df = df_selection
        else:
            self.df = pd.concat([self.df, df_selection])

    def get_metrics(
        self,
        st: float,
        et: float,
        sources,
        org_uid: str,
        api_key: str,
        api_url: str,
    ) -> Iterable:
        st = int(st)
        et = int(et)

        # pipeline = [{"filter": {"schema": "event_metric:agent"}}]
        metrics = retrieve_data(
            api_url,
            api_key,
            org_uid,
            sources,
            datatype="agent_status",
            schema="event_metric:agent",
            time=(st, et),
            # pipeline,
            # limit_mem=False,
            disable_pbar=True,
            projection_func=metric_project,
        )
        return metrics

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
        mdx_context = deepcopy(context)
        mdx_context["st"] = datetime.fromtimestamp(context["st"], timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S %Z"
        )
        mdx_context["et"] = datetime.fromtimestamp(context["et"], timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S %Z"
        )
        summary_grid = self.make_summary_grid(context["metrics_summary"])
        mdx_context["metrics_summary"]["grid"] = summary_grid

        for metric in ["cpu", "mem", "bps"]:
            agent_grid = self.make_agent_grid(context["agent_metrics"], metric)
            mdx_context["agent_metrics"][metric] = {}
            mdx_context["agent_metrics"][metric]["grid"] = agent_grid
        return mdx_context

    def make_agent_grid(self, agent_metrics: dict, metric: str) -> str:
        match metric:
            case "cpu":
                type = None
            case "mem":
                type = "bytes"
            case "bps":
                type = "bytesPerSecond"
            case _:
                raise ValueError(f"Invalid metric: {metric}")
        columns = [
            {"title": "Agent", "field": "agent"},
            {
                "title": "Mean",
                "field": "mean",
            },
            {
                "title": "P90",
                "field": "p90",
            },
            {
                "title": "P99",
                "field": "p99",
            },
        ]
        if type:
            for col in columns:
                col["type"] = type
        data = [
            {
                "id": index,
                "agent": stats["name"],
                "mean": round(stats[metric]["mean"], 3),
                "p90": round(stats[metric]["p90"], 3),
                "p99": round(stats[metric]["p99"], 3),
            }
            for index, stats in enumerate(agent_metrics.values())
        ]
        return mdx_lib.make_grid(columns, data)

    def make_summary_grid(self, summary: dict) -> str:
        columns = [
            {"title": "Metric", "field": "metric"},
            {
                "title": "Mean",
                "field": "mean",
            },
            {
                "title": "P90",
                "field": "p90",
            },
            {
                "title": "P99",
                "field": "p99",
            },
        ]
        data = [
            {
                "metric": "CPU load",
                "mean": round(summary["cpu"]["mean"], 3),
                "p90": round(summary["cpu"]["p90"], 3),
                "p99": round(summary["cpu"]["p99"], 3),
            },
            {
                "metric": "Memory (MB)",
                "mean": f'{round(summary["mem"]["mean"] / 1048576)} MB',
                "p90": f'{round(summary["mem"]["p90"] / 1048576)} MB',
                "p99": f'{round(summary["mem"]["p99"] / 1048576)} MB',
            },
            {
                "metric": "Bandwidth (bytes/sec)",
                "mean": f'{round(summary["bps"]["mean"])}',
                "p90": f'{round(summary["bps"]["p90"])}',
                "p99": f'{round(summary["bps"]["p99"])}',
            },
        ]
        return mdx_lib.make_grid(columns, data)
