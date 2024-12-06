from bs_monitoring.monitors import create_monitors, Monitor
from bs_monitoring.alert_services import create_alert_service
from bs_monitoring.data_sources import create_data_source, DataSource
from bs_monitoring.databases import initialize_databases
from bs_monitoring.common.configs.base import RootConfig


class Pipeline:
    def __init__(self, source: DataSource, monitors: list[Monitor]):
        self.source = source
        self.monitors = monitors

    @staticmethod
    def construct(config: RootConfig):
        initialize_databases(config.Databases)

        alert_service = create_alert_service(config.AlertService)
        source = create_data_source(config.DataSource, alert_service)
        monitors = create_monitors(config.Monitors, alert_service)

        return Pipeline(source, monitors)

    def run(self):
        data = self.source.produce()

        for m in self.monitors:
            m.process(data)
