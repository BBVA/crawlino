import logging

from crawlino import extractor_plugin, PluginReturnedData

log = logging.getLogger("crawlino-plugins")


@extractor_plugin
def extractor_xpath(prev_step: PluginReturnedData, **kwargs) \
        -> PluginReturnedData:

    log.debug("Starting plugin - extractor::xpath")

    d = PluginReturnedData(**dict(hola="mundo"))

    return d