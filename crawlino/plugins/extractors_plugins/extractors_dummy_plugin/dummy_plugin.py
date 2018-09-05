import logging

from crawlino import extractor_plugin, PluginReturnedData

log = logging.getLogger("crawlino-plugins")


@extractor_plugin
def extractor_dummy(prev_stepPluginReturnedData, **kwargs) \
        -> PluginReturnedData:
    log.debug("Extractor Module :: dummy plugin")

    d = PluginReturnedData(**dict(dummy="plugin"))

    return d
