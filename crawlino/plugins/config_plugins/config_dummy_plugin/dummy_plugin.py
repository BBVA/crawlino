import logging

from crawlino import config_plugin, PluginReturnedData

log = logging.getLogger("crawlino-plugin")


@config_plugin
def config_dummy(prev_step: PluginReturnedData, **kwargs):
    log.debug("Config Module :: dummy plugin")
