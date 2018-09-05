import re
import logging

from crawlino import extractor_plugin, PluginReturnedData, CrawlinoValueError

log = logging.getLogger("crawlino-plugins")


@extractor_plugin
def extractor_regex(prev_step: PluginReturnedData, **kwargs) \
        -> PluginReturnedData:

    log.debug("Starting plugin - extractor::xpath")

    #
    # Applying expressions
    #
    try:
        expressions = kwargs["expressions"]
    except KeyError:
        raise CrawlinoValueError(
            "You can't run a rule without expressions")

    content_to_analyze = kwargs["content"]
    regex_group = kwargs.get("reportGroup", None)

    result = None
    if content_to_analyze:
        content_to_analyze = str(content_to_analyze)

        for expression in expressions:
            # Remove last \n
            if expression[-1] == "\n":
                expression = expression[:-1]

            if regex_group:
                try:
                    found = re.search(expression, content_to_analyze)
                except TypeError as e:
                    log.debug(e)
                    continue

                if found:
                    try:
                        regex_group = int(regex_group)
                    except ValueError:
                        raise CrawlinoValueError(
                            f"Invalid 'reportGroup'. Value must be an integer")

                    result = found.group(regex_group)
                    break
            else:
                for line in content_to_analyze.splitlines():
                    try:
                        if re.search(expression, line):
                            result = line
                            break
                    except TypeError as e:
                        log.error(e)

    d = PluginReturnedData(**dict(
        content=result
    ))

    return d
