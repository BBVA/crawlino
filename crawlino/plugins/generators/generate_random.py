import random
import string
import logging

from crawlino import generator_plugin, CrawlinoValueError

log = logging.getLogger("crawlino-plugin")


@generator_plugin
def generator_random(*args, **kwargs):
    """
    Input parameters:

    arg[0]: generated type: string, number
    arg[1]: generated value len
    arg[2]: total of random values generated
    """
    generated_type, maximum, total = args

    space = string.digits
    if generated_type == "string":
        space += string.ascii_letters

    if total <= 0:
        raise CrawlinoValueError(
            f"Total generated values must be bigger than 0")

    for _ in range(total):
        yield "".join(random.choice(space) for _ in range(maximum))
