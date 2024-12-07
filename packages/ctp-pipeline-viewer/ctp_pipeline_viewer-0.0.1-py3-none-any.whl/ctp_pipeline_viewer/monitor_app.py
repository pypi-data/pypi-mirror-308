import collections
import functools
import math
from datetime import datetime
from typing import DefaultDict

import textual_plotext
import xnat
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.timer import Timer
from textual.widgets import Header, TabbedContent, TabPane, Footer, Label
from textual_plotext import PlotextPlot
from xnat.session import XNATSession

from src.ctp_pipeline_viewer.ctp_processing import get_ctp_summary
from src.ctp_pipeline_viewer.data_types import (
    ProjectConfig, CtpSummary, XnatExperimentInfo, has_ctp_views, has_xnat_views, View, Configs)
from src.ctp_pipeline_viewer.xnat_processing import xnat_experiment_info


def _elapsed_seconds(_timestamp: datetime, _now: datetime) -> int:
    return math.ceil((_timestamp - _now).total_seconds())


class PipelineMonitor(App):
    def __init__(self, configs: Configs) -> None:
        super().__init__()
        self.configs = configs

        # History of the CTP and XNAT data
        self.ctp_history: DefaultDict[str, list[CtpSummary]] = collections.defaultdict(
            functools.partial(collections.deque, maxlen=self.configs.history))  # type: ignore
        self.xnat_history: DefaultDict[str, list[XnatExperimentInfo]] = collections.defaultdict(
            functools.partial(collections.deque, maxlen=self.configs.history))  # type: ignore

        self._timer: Timer | None = None
        self._sessions: dict[str, XNATSession] = {}

    def __del__(self) -> None:
        for session in self._sessions.values():
            session.disconnect()

    @functools.cached_property
    def _pipeline_from_project(self) -> dict[str, str]:
        return {config.xnat_project: config.ctp_pipeline for config in self.configs.configs if
                config.xnat_project is not None and config.ctp_pipeline is not None}

    @functools.cached_property
    def _project_from_pipeline(self) -> dict[str, str]:
        return {config.ctp_pipeline: config.xnat_project for config in self.configs.configs if
                config.xnat_project is not None and config.ctp_pipeline is not None}

    @functools.cached_property
    def _pipelines(self) -> list[str]:
        return [config.ctp_pipeline for config in self.configs.configs]

    def on_mount(self) -> None:
        self._timer = self.set_interval(self.configs.interval, self._timer_elapsed)
        for _ in range(self.configs.history):
            for pipeline in self._pipelines:
                config = self._get_config(pipeline)

                if has_ctp_views(config):
                    self.ctp_history[pipeline].append(CtpSummary())

                if config.xnat_url is not None and has_xnat_views(config):
                    self.xnat_history[pipeline].append(XnatExperimentInfo())

        self.update_plots()

    def compose(self) -> ComposeResult:
        yield Header(name='CTP Pipelines', show_clock=True)
        with TabbedContent():
            for pipeline in self._pipelines:
                with TabPane(pipeline, id=f'tab_{pipeline}'):
                    with Vertical():
                        yield PlotextPlot(id=f'plot_{pipeline}')
                        yield Label(id=f'label_{pipeline}')
        yield Footer()

    def _get_config(self, pipeline: str) -> ProjectConfig:
        for config in self.configs.configs:
            if config.ctp_pipeline == pipeline:
                return config
        raise ValueError(f'{pipeline} not found.')

    async def _timer_elapsed(self) -> None:
        self.ctp_timer_elapsed()
        self.xnat_timer_elapsed()

    @work
    async def ctp_timer_elapsed(self) -> None:
        ctp_results = await get_ctp_summary(list({x.ctp_url + '/summary?suppress' for x in self.configs.configs}))

        for val in ctp_results:
            self.ctp_history[val.pipeline].append(val)

        self.update_plots()

    @work
    async def xnat_timer_elapsed(self) -> None:
        xnat_servers: collections.defaultdict[str, list[tuple[str, list[View]]]] = collections.defaultdict(list)
        for config in self.configs.configs:
            if config.xnat_url is None or config.xnat_project is None:
                continue
            xnat_servers[config.xnat_url].append((config.xnat_project, config.views))

        for server, projects in xnat_servers.items():
            xnat_results = xnat_experiment_info(self._get_xnat_session(server), projects)
            for project, result in xnat_results.items():
                self.xnat_history[self._pipeline_from_project[project]].append(result)

        # Update the plots
        self.update_plots()

    def _get_xnat_session(self, server: str) -> xnat.XNATSession:
        if server in self._sessions:
            return self._sessions[server]

        session = xnat.connect(server)
        self._sessions[server] = session
        return session

    def update_plots(self) -> None:
        for pipeline in self._pipelines:
            config = self._get_config(pipeline)
            num_views = len(config.views)

            plotextplot = self.query_one(f'#plot_{pipeline}', PlotextPlot)
            plt = plotextplot.plt
            plt.clear_figure()
            plt.subplots(num_views)

            index = 1
            if has_ctp_views(config):
                index = self._ctp_plots(pipeline, plt, config.views, index)
            if has_xnat_views(config):
                self._xnat_plots(pipeline, plt, config.views, index)

            plotextplot.refresh()

            self.query_one(f'#label_{pipeline}', Label).update(self.pipeline_text(config, pipeline))

    def pipeline_text(self, config: ProjectConfig, pipeline: str) -> str:
        label_text = ''

        if has_ctp_views(config):
            last_ctp: CtpSummary = self.ctp_history[pipeline][-1]
            for view in config.views:
                match view:
                    case View.IMPORT_QUEUE:
                        label_text += f'Import: {last_ctp.import_queues} '
                    case View.EXPORT_QUEUE:
                        label_text += f'Export: {last_ctp.export_queues} '
                    case View.QUARANTINES:
                        label_text += f'Quarantines: {last_ctp.quarantines} '

        if has_xnat_views(config):
            last_xnat: XnatExperimentInfo = self.xnat_history[pipeline][-1]
            for view in config.views:
                match view:
                    case View.ARCHIVE:
                        label_text += f'Archive: {len(last_xnat.archive)} '
                    case View.PRE_ARCHIVE:
                        label_text += f'Pre-archive: {len(last_xnat.pre_archive)} '

        return label_text

    def _ctp_plots(self, pipeline: str, plt: textual_plotext.Plot, views: list[View], index: int) -> int:
        start = self.ctp_history[pipeline][0].time_stamp
        end = self.ctp_history[pipeline][-1].time_stamp

        now = datetime.now()
        timestamps = [_elapsed_seconds(x.time_stamp, now) for x in self.xnat_history[pipeline]]

        if View.IMPORT_QUEUE in views:
            color = 'red+'
            sub = plt.subplot(index, 1)
            index += 1
            sub.title(f'Import Queue {start:%H:%M:%S} - {end:%H:%M:%S}')
            sub.plot(timestamps, [x.import_queues for x in self.ctp_history[pipeline]], color=color)

        if View.EXPORT_QUEUE in views:
            color = 'orange+'
            sub = plt.subplot(index, 1)
            index += 1
            sub.title(f'Export Queue {start:%H:%M:%S} - {end:%H:%M:%S}')
            sub.plot(timestamps, [x.export_queues for x in self.ctp_history[pipeline]], color=color)

        if View.QUARANTINES in views:
            color = 'orange'
            sub = plt.subplot(index, 1)
            index += 1
            sub.title(f'Quarantines {start:%H:%M:%S} - {end:%H:%M:%S}')
            sub.plot(timestamps, [x.quarantines for x in self.ctp_history[pipeline]], color=color)

        return index

    def _xnat_plots(self, pipeline: str, plt: textual_plotext.Plot, views: list[View], index: int) -> int:
        start = self.xnat_history[pipeline][0].time_stamp
        end = self.xnat_history[pipeline][-1].time_stamp

        now = datetime.now()
        timestamps = [_elapsed_seconds(x.time_stamp, now) for x in self.xnat_history[pipeline]]

        if View.ARCHIVE in views:
            color = 'green+'
            sub = plt.subplot(index, 1)
            index += 1
            sub.title(f'Archive {start:%H:%M:%S} - {end:%H:%M:%S}')
            sub.plot(timestamps, [len(x.archive) for x in self.xnat_history[pipeline]], color=color)

        if View.PRE_ARCHIVE in views:
            color = 'cyan+'
            sub = plt.subplot(index, 1)
            index += 1
            sub.title(f'Pre-Archive {start:%H:%M:%S} - {end:%H:%M:%S}')
            sub.plot(timestamps, [len(x.pre_archive) for x in self.xnat_history[pipeline]], color=color)

        return index
