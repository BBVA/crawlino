import logging

from typing import List

from crawlino import source_plugin, SourceData, PluginReturnedData

log = logging.getLogger("crawlino-plugin")


@source_plugin
def source_dummy(prev_step: PluginReturnedData, **kwargs) \
        -> List[SourceData] or SourceData:

    d = SourceData("file://dummy/module/runs")

    log.debug("Sources Module :: dummy plugin")

    return d
