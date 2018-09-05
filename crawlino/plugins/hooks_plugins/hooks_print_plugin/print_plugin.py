import json
import logging

from crawlino import hook_plugin, PluginReturnedData, CrawlinoValueError

log = logging.getLogger("crawlino-plugin")


@hook_plugin
def hook_print(prev_step: PluginReturnedData, **kwargs):
    log.debug("Hooks Module :: print plugin")

    allowed_output_format = ("json", "csv")

    data = prev_step.to_dict
    if not data:
        return

    config = kwargs.get("config", {})
    output_format = config.get("format", "json")

    # -------------------------------------------------------------------------
    # Check the source of data. If data comes from step: expressions, check if
    # there're results. If not have results -> don't display nothing
    #
    # Data from STEP_EXTRACTORS have property: 'extractor_results'
    # -------------------------------------------------------------------------
    if "extractor_results" in data:
        if not data["extractor_results"]:
            # No data to display
            return

    if output_format not in allowed_output_format:
        raise CrawlinoValueError(
            f"Invalid output format value '{output_format}'. Allowed values "
            f"are: {'|'.join(allowed_output_format)}")

    if output_format == "json":
        # We need to use the 'default' arg because for inherit dicts, json
        # module some times raises TypeError exception
        print(json.dumps(data,
                         default=lambda x: dict(x.to_dict)
                         if hasattr(x, "to_dict") else dict(x),
                         indent=4,
                         sort_keys=True))

    elif output_format == "csv":
        l = []
        for k, v in data.items():
            l.append(f"'{k}:{v}'")

        print(", ".join(l))