import os
import logging
import os.path as op

from crawlino import generator_plugin, CrawlinoValueError

log = logging.getLogger("crawlino-plugin")


@generator_plugin
def generator_wordlist(*args, **kwargs):
    """This generator create sequences of numbers from: art[0] to arg[1]"""
    log.debug("Numeric generator plugin")

    wordlist_base_path = op.abspath(op.join(op.dirname(__file__),
                                            "..",
                                            "..",
                                            "wordlist"))

    for wordlist in args:

        # Try to locate the wordlist
        name, extension = op.splitext(wordlist)

        ws_file = op.join(wordlist_base_path, f"{name}.txt")

        with open(ws_file, "r") as w:
            for word in w.readlines():
                yield word.replace("\n", "")
