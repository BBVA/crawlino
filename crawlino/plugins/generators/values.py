import logging

from crawlino import generator_plugin, CrawlinoValueError

log = logging.getLogger("crawlino-plugin")


@generator_plugin
def generator_values(*args, **kwargs):
    """This generator produces the values passed as args input"""
    log.debug("Values generator plugin")

    for x in args:
        yield x
