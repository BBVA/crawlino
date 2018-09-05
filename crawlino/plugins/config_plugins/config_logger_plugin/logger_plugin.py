import logging

from crawlino import config_plugin, dict_to_object, PluginReturnedData

log = logging.getLogger("crawlino-plugin")


@config_plugin
def config_logger(prev_step: PluginReturnedData, **kwargs):
    """
    This plugin configures the loggers
    """
    loaded_data = dict_to_object(kwargs)

    log.debug("Config Module :: dummy plugin")


    # tmp_logger = gt(model, "logger", "crawlino")
    #
    # if tmp_logger and not isinstance(tmp_logger, Iterable):
    #     raise CrawlinoValueError("logger should be a list")
    #
    # # --------------------------------------------------------------------------
    # # Fill logger
    # # --------------------------------------------------------------------------
    # self.logger = []
    # for l in tmp_logger:
    #     l_name = l.get("type", "crawlino")
    #     l_level = l.get("logLevel", None)
    #
    #     if l_level and type(l_level) is not int:
    #         raise CrawlinoValueError("LogLevel must be an integer value")
    #
    #     self.logger.append(LoggerModel(type=l_name, logLevel=l_level))