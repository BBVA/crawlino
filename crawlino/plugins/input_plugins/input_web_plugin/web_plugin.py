import json
import logging
import requests
import urllib.parse

from crawlino import input_plugin, PluginReturnedData, \
    dict_to_object, CrawlinoValueError

log = logging.getLogger("crawlino-plugins")


@input_plugin
def input_web(prev_step: PluginReturnedData, **kwargs) -> PluginReturnedData:
    log.debug("Starting plugin - input::web")

    allowed_inputs = ("web", "domain")

    # Load data
    prev_config = dict_to_object(prev_step.to_dict)

    if prev_config.source_type not in allowed_inputs:
        raise CrawlinoValueError(f"This plugin only works with: "
                                 f"{'|'.join(allowed_inputs)}")

    # --------------------------------------------------------------------------
    # Extract config
    # --------------------------------------------------------------------------
    config = kwargs.get("config", {})
    timeout = config.get("timeout", "0.5").lower()
    http_method = config.get("httpMethod", "GET").lower()
    http_type = config.get("contentType", None)
    http_headers = {
        x: y
        for x, y in config.get("httpHeaders", {}).items()
    }
    http_url = config.get("url", "")
    post_data = None
    if config.get("data", None) and http_method in ("post", "put", "delete"):
        if http_type == "":
            # Request only accept post data as format:
            # [("id", "value"), ("user", "value2")]
            post_data = [
                x.split("=") for x in config.get("data", "").split("&")
            ]

        elif http_type == "json" or http_type == "application/json":
            post_data = config.get("data", "")
            http_headers["Content-Type"] = "application/json"

    #
    # Fix target
    #
    url_parsed = urllib.parse.urlparse(prev_config.target)
    if not url_parsed.scheme:
        target = f"http://{url_parsed.netloc}"
    else:
        target = f"{url_parsed.scheme}://{url_parsed.netloc}"

    #
    # Fix target URL
    #
    url = f"{target}{http_url}"

    try:
        response = requests.request(
            method=http_method,
            url=url,
            headers=http_headers,
            data=post_data,
            timeout=float(timeout)
        )
    except Exception as e:
        log.debug(e)
        return PluginReturnedData()

    else:
        result = dict(
            status_code=response.status_code,
            headers=response.headers,
            content=response.text,
            request=dict(
                method=http_method,
                url=url,
                headers=http_headers,
                data=post_data
            )
        )

        d = PluginReturnedData(**result)

        return d
