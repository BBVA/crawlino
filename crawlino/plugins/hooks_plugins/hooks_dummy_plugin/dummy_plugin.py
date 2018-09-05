import logging

from crawlino import hook_plugin, PluginReturnedData

log = logging.getLogger("crawlino-plugin")


@hook_plugin
def hook_dummy(prev_step: PluginReturnedData, **kwargs):
    log.debug("Hook Module :: dummy plugin")
