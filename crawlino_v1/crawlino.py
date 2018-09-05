import inspect
import logging
import requests
import lxml.html
import os.path as op

from lxml import etree
from typing import Union
from argparse import Namespace

from crawlino import load_crawlino_json, CrawlinoContent, load_model, \
    model_map_2_orm_model
from crawlino.transforms import camelcase2underscore, auto_setter, \
    html2simple_html, html2plain_text

log = logging.getLogger("crawlino")


class _CrawlinoV1:

    def __init__(self,
                 crawler_name: str,
                 *,
                 definition_path: str = None,
                 extra_log_info: str = None):

        self._iter_pos = 0
        self.crawler_name = crawler_name
        self.extra_log_info = extra_log_info

        if not definition_path:
            config_file_name = "crawlino_{}.json".format(
                # My Crawler Name -> my_crawler_name
                camelcase2underscore(self.crawler_name)
            )

            # Get file where _CrawlinoV1 class is called
            caller_file_name = inspect.getmodule(
                inspect.stack()[1][0]).__file__

            # Locate and set the JSON file in the same directory and with the
            # name os crawler in underscore format. I.e:
            #   My Custom Crawler -> crawlino_my_custom_crawler.json
            self.definition_path = op.abspath(
                op.join(
                    op.dirname(
                        caller_file_name), config_file_name))
        else:
            self.definition_path = definition_path

        self.config = self._load_crawler_config_()
        self.log = logging.getLogger(self.config.logName)

    # --------------------------------------------------------------------------
    # Custom XPath functions
    # --------------------------------------------------------------------------
    def _advanced_xpath(self,
                        obj,
                        xpath: str,
                        var_name: str,
                        *,
                        property_to_get: str = "text",
                        to_lower: bool = True,
                        show_error_log: bool = True,
                        capitalize: bool = True,
                        append: bool = False) -> str or None:
        """
        :param property_to_get: si se usa "raw", devolvera todo el contenido
        del html tal cual. Con "plain" transformara el HTML en texto plano.
        :type property_to_get:
        """
        try:
            if append:
                rows = obj.xpath(xpath)
            else:
                rows = [obj.xpath(xpath)[0]]

            results = []

            for row in rows:
                if property_to_get == "text":
                    result = getattr(row, "text", row)
                elif property_to_get == "plain":
                    result = row.text_content()
                elif property_to_get == "raw":
                    try:
                        result = etree.tostring(row).decode()
                    except TypeError:
                        result = row

                else:
                    try:
                        result = row.get(property_to_get)
                    except AttributeError:

                        log.error("Error while trying to apply a rule",
                                  exc_info=True,
                                  extra=dict(
                                      error_in_property=property_to_get,
                                      var_name=var_name,
                                      xpath_expression=xpath,
                                      crawler_name=self.crawler_name
                                  ))

                        result = ""

                if to_lower and result:
                    result = result.lower()

                    if capitalize and result:
                        result = result.capitalize()

                if result:
                    results.append(result)

            if results:
                return "\n".join(results)
            else:
                return None

        except IndexError:
            if show_error_log:
                log.error("Error while try to apply a crawler rule",
                          exc_info=True,
                          extra=dict(
                              extra_info=self.extra_log_info,
                              var_name=var_name,
                              xpath_expression=xpath,
                              crawler_name=self.crawler_name
                          ))

                # self.log.info(
                #     'Crawler "{}" >> Keywork: "{}" no encontrada '
                #     'con la regla: "{}" --- Extra log: "{}"'.format(
                #         self.crawler_name,
                #         var_name,
                #         xpath,
                #         self.extra_log_info))

    def _massive_advanced_xpath(self,
                                content: etree.ElementTree,
                                field_name: str,
                                rules: list,
                                *,
                                to_lower: bool = True,
                                capitalize: bool = True,
                                append: bool = False) -> str:

        total_expressions = len(rules)

        for i, e in enumerate(rules, start=1):
            _expression = e.expression
            _property = e.property
            _raise_log = total_expressions == i

            r = self._advanced_xpath(content,
                                     _expression,
                                     field_name,
                                     capitalize=capitalize,
                                     property_to_get=_property,
                                     show_error_log=_raise_log,
                                     append=append,
                                     to_lower=to_lower)

            if r:
                return r

    def _load_crawler_config_(self):
        config = load_crawlino_json(self.definition_path)

        # --------------------------------------------------------------------------
        # Load Models, if needed
        # --------------------------------------------------------------------------
        _models_to_load = [c.modelMap for c in config.crawlers]
        self.models = {}
        for _model_name in _models_to_load:
            for _model in config.models:
                if _model.name != _model_name:
                    continue

                self.models[_model_name] = Namespace(
                    ormType=_model.ormType,
                    model=load_model(_model.model)
                )

        return config

    # -------------------------------------------------------------------------
    # Iterator definition
    # -------------------------------------------------------------------------
    def __iter__(self):

        log.debug("Looking for main Crawler")
        self.main_crawler = self.config.crawlers[int(
            "".join(str(i) for i, x in enumerate(self.config.crawlers)
                    if x.mainCrawler is True)
        )]

        # ---------------------------------------------------------------------
        # Download the URL content & set main crawler
        # ---------------------------------------------------------------------
        log.debug("Downloading content from Main Crawler",
                  extra={"crawler_name": self.crawler_name})
        self.main_crawler_content = requests.get(
            self.main_crawler.startUrl).text

        log.debug("Parsing content")
        parsed = lxml.html.fromstring(self.main_crawler_content)
        if self.main_crawler.contentIterator:
            self.main_start_object = parsed.xpath(
                self.main_crawler.contentIterator)
        else:
            self.main_start_object = parsed

        return self

    def __next_item__(self):
        # Get next element to process
        try:
            content_etree = self.main_start_object[self._iter_pos]
            self._iter_pos += 1
            return content_etree
        except IndexError:
            raise StopIteration

    def __next__(self) -> CrawlinoContent:

        field_data = {}
        content_etree = self.__next_item__()

        # For each content object check all the fields
        for field in self.main_crawler.fields:

            _extra_params = {
                "capitalize": field.capitalize,
                "append": True
            }

            content_found = self._massive_advanced_xpath(
                content_etree,
                field.name,
                field.rules,
                **_extra_params
            )

            # --------------------------------------------------------------------------
            # Optional / Mandatory
            # --------------------------------------------------------------------------
            if not content_found:
                field_data[field.name] = None

            if field.mandatory and not content_found:
                log.info("Can't continue due rules for field '{}' "
                         "doesn't return content".format(field.name),
                         extra=dict(
                             crawler_name=self.crawler_name,
                             field_name=field.name
                         ),
                         exc_info=True)
                return

            elif content_found:
                field_data[field.name] = content_found

            else:
                _field_content = None
                if field.autoSet:
                    _field_content = auto_setter(field.type)

                field_data[field.name] = _field_content

            # --------------------------------------------------------------------------
            # ModuleData transforms
            # --------------------------------------------------------------------------
            if field.transforms:
                if field.transforms == "plainHTML":
                    field_data[field.name] = html2simple_html(content_found)
                elif field.transforms == "plainText":
                    field_data[field.name] = html2plain_text(content_found)

        # --------------------------------------------------------------------------
        # Add fixed fields before return model
        # --------------------------------------------------------------------------
        for fixed in self.main_crawler.fixedFields:
            field_data.update({
                fixed.name: fixed.value
            })

        # --------------------------------------------------------------------------
        # Map to model?
        # --------------------------------------------------------------------------
        ret = CrawlinoContent(
            content_etree,
            field_data
        )

        if self.main_crawler.modelMap:
            ret.model_obj = model_map_2_orm_model(
                field_data,
                self.models[self.main_crawler.modelMap])

        return ret


Crawlino = _CrawlinoV1

__all__ = ("Crawlino",)
