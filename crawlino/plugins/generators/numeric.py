import logging

from crawlino import generator_plugin, CrawlinoValueError

log = logging.getLogger("crawlino-plugin")


@generator_plugin
def generator_numeric(*args, **kwargs):
    """This generator create sequences of numbers from: art[0] to arg[1]"""
    log.debug("Numeric generator plugin")

    start, end, *_ = args

    if start > end:
        raise CrawlinoValueError(
            f"Start range in higher than lower, no data could be generated - "
            f"start: {start} - end: {end}")

    for x in range(start, end):
        yield x
