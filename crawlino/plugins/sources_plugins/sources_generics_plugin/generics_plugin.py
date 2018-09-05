import logging

from typing import List

from crawlino import source_plugin, SourceData, CrawlinoValueError, \
    PluginReturnedData

log = logging.getLogger("crawlino-plugin")


def _build(**kwargs):
    config = kwargs.get("config")
    valid_properties = ("url", "domain", "ip")

    for x in valid_properties:
        if x in config:
            target = config[x]
            break
    else:
        raise CrawlinoValueError(
            f"Selected source type must have any of these properties: "
            f"{'|'.join(valid_properties)}")

    return SourceData(target)


@source_plugin
def source_domain(prev_step: PluginReturnedData, **config) -> List[SourceData] or SourceData:

    log.debug("Sources Module :: domain plugin")

    return _build(**config)


@source_plugin
def source_url(prev_step: PluginReturnedData, **config) -> List[SourceData] or SourceData:
    log.debug("Sources Module :: url plugin")

    return _build(**config)


@source_plugin
def source_web(prev_step: PluginReturnedData, **config) -> List[SourceData] or SourceData:
    log.debug("Sources Module :: web plugin")

    return _build(**config)


@source_plugin
def source_ip(prev_step: PluginReturnedData, **config) -> List[SourceData] or SourceData:
    log.debug("Sources Module :: web plugin")

    return _build(**config)
