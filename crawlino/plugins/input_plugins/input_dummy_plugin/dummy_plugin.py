import logging

from crawlino import input_plugin, PluginReturnedData

log = logging.getLogger("crawlino-plugins")


@input_plugin
def input_dummy(prev_step: PluginReturnedData, **kwargs) \
        -> PluginReturnedData:
    log.debug("Input Module :: dummy plugin")

    d = PluginReturnedData(**dict(dummy="plugin"))

    return d
