import json
import logging

from typing import Union, List, Dict
from argparse import Namespace

from ..exceptions import CrawlinoFormatError, CrawlinoValueError
from crawlino.exceptions import CrawlinoMainCrawlerNotFound, \
    CrawlinoMainCrawlerDuplicated

log = logging.getLogger("crawlino")

ALLOWED_CONFIGURATION_FILES_FORMAT = ("json",)

MODEL_ORM_TYPES = ("sqlAlchemy", )
MODEL_FIELDS_TYPES = ("text", "datetime", "number")
CRAWLER_FIELDS_TYPES = MODEL_FIELDS_TYPES + ("link", )
CRAWLER_RULES_PROPERTIES = ("href", "datetime", "text", "raw")
CRAWLER_FIELDS_TRANSFORMS = ("plainHTML", "plainText")

# --------------------------------------------------------------------------
# Map the function to do code shorter
# --------------------------------------------------------------------------
gt = getattr


# --------------------------------------------------------------------------
# Parser aux functions
# --------------------------------------------------------------------------
def _parse_crawlers_definitions(crawlers_obj: List[Dict]) -> List[Namespace]:
    for c in crawlers_obj:
        _crawler_name = gt(c, "name", None)
        _crawler_start_url = gt(c, "startUrl", None)
        _crawler_content_iterator = gt(c, "contentIterator", None)
        _crawler_model_map = gt(c, "modelMap", None)
        _crawler_main_crawler = gt(c, "mainCrawler", False)
        _crawler_fixed_fields = gt(c, "fixedFields", [])

        if not _crawler_name:
            log.error("Error in crawlers: "
                      "Crawlers must have 'name' property.")
            continue

        if not _crawler_start_url:
            log.error("Error in crawler '{}': "
                      "Crawlers needs 'startUrl' property.".format(
                _crawler_name
            ))
            continue

        if type(_crawler_main_crawler) is not bool:
            log.warning("Invalid 'mainCrawler' property type in crawler: '{}'"
                        ". Type must be Boolean".format(
                _crawler_name
            ))
            continue

        # ---------------------------------------------------------------------
        # Load fields
        # ---------------------------------------------------------------------
        _crawler_fields = []
        for _field in gt(c, "fields", []):
            _crawler_field_name = gt(_field, "name", None)
            _crawler_field_type = gt(_field, "type", "text")
            _crawler_field_mandatory = gt(_field, "mandatory", False)
            _crawler_field_capitalize = gt(_field, "capitalize", False)
            _crawler_field_auto_set = gt(_field, "autoSet", False)
            _crawler_field_transforms = gt(_field, "transforms", None)

            if not _crawler_field_name:
                log.warning("Error in fields in Crawler '{}': "
                            "A field must have a 'name' property.".format(
                    _crawler_name
                ))
                continue

            if _crawler_field_type not in MODEL_FIELDS_TYPES:
                log.warning("Invalid field type '{}' for field name '{}' "
                            "in crawler: '{}'".format(
                    _crawler_field_type,
                    _crawler_field_name,
                    _crawler_name
                ))
                continue

            if _crawler_field_transforms and \
                            _crawler_field_transforms not in \
                            CRAWLER_FIELDS_TRANSFORMS:
                log.warning("Invalid property 'transforms' in "
                            "field '{}' in crawler: '{}'".format(
                    _crawler_field_name,
                    _crawler_name
                ))
                continue

            if type(_crawler_field_mandatory) is not bool:
                log.warning("Invalid 'mandatory' property in crawler: '{}'. "
                            "Type must be Boolean".format(
                    _crawler_name
                ))
                continue

            if type(_crawler_field_capitalize) is not bool:
                log.warning("Invalid 'capitalize' property in crawler: '{}'. "
                            "Type must be Boolean".format(
                    _crawler_name
                ))
                continue

            if type(_crawler_field_auto_set) is not bool:
                log.warning("Invalid 'autoSet' property in crawler: '{}'. "
                            "Type must be Boolean".format(
                    _crawler_name
                ))
                continue

            # -----------------------------------------------------------------
            # Load Rules
            # -----------------------------------------------------------------
            _crawler_fields_rules = []
            for _rule in gt(_field, "rules", []):
                _rule_expression = gt(_rule, "expression", None)
                _rule_property = gt(_rule, "property", None)

                if not _rule_expression:
                    log.warning("Error in Crawler '{}'. Field '{}'. Rules "
                                "must have 'expression' property.")
                    continue

                if _rule_property not in CRAWLER_RULES_PROPERTIES:
                    log.warning("Invalid property type '{}' in expression '{}'"
                                ", in field name '{}' in crawler: '{}'".format(
                        _rule_property,
                        _rule_expression,
                        _crawler_field_name,
                        _crawler_name
                    ))
                    continue

                _crawler_fields_rules.append(Namespace(
                    expression=_rule_expression,
                    property=_rule_property
                ))

            _crawler_fields.append(Namespace(
                name=_crawler_field_name,
                mandatory=_crawler_field_mandatory,
                capitalize=_crawler_field_capitalize,
                autoSet=_crawler_field_auto_set,
                transforms=_crawler_field_transforms,
                type=_crawler_field_type,
                rules=_crawler_fields_rules
            ))

        # ---------------------------------------------------------------------
        # Store fields in Crawlers
        # ---------------------------------------------------------------------
        return_obj.crawlers.append(Namespace(
            name=_crawler_name,
            mainCrawler=_crawler_main_crawler,
            startUrl=_crawler_start_url,
            contentIterator=_crawler_content_iterator,
            modelMap=_crawler_model_map,
            fixedFields=_crawler_fixed_fields,
            fields=_crawler_fields
        ))


def _parse_model_definitions(models_obj: List[Dict]) -> List[Namespace]:
    for model in models_obj:
        _model_name = gt(model, "name", None)
        _model_model = gt(model, "model", None)
        _model_orm_type = gt(model, "ormType", None)

        if not _model_name:
            log.error("Error in Models: "
                      "Models must have 'name' property.")
            continue

        if _model_orm_type and _model_orm_type not in MODEL_ORM_TYPES:
            log.error("Invalid 'ormType' property for Model '{}'. Available"
                      " values are: {}".format(
                _model_name,
                ", ".join(MODEL_ORM_TYPES)
            ))

        # ---------------------------------------------------------------------
        # Extract Model fields
        # ---------------------------------------------------------------------
        _fields = []
        for _field in gt(model, "fields", []):
            _crawler_field_name = gt(_field, "name", None)
            _crawler_field_type = gt(_field, "type", "text")

            if not _crawler_field_name:
                log.warning("Error in fields in Model '{}': "
                            "A field must have a 'name' property.".format(
                    _model_name
                ))
                continue

            if _crawler_field_type not in MODEL_FIELDS_TYPES:
                log.warning("Invalid field type '{}' for field name '{}' "
                            "in model: '{}'".format(
                    _crawler_field_type,
                    _crawler_field_name,
                    _model_name
                ))
                continue

            # If not errors -> Store field type
            _fields.append(
                Namespace(
                    name=_crawler_field_name,
                    type=_crawler_field_type
                )
            )

        # ---------------------------------------------------------------------
        # Store fields in model
        # ---------------------------------------------------------------------
        return_obj.models.append(Namespace(
            name=_model_name,
            ormType=_model_orm_type,
            model=_model_model,
            fields=_fields
        ))


# --------------------------------------------------------------------------
# Parser main function
# --------------------------------------------------------------------------
def _parse_crawlino_definition(config_obj: dict) -> \
        Union[Namespace,
              CrawlinoFormatError,
              CrawlinoMainCrawlerNotFound]:
    """This function parses configuration file loaded as a dict format"""

    return_obj = Namespace()

    # Crawler definition are mandatory
    if gt(config_obj, "extractors") in (None, []):
        raise CrawlinoFormatError("All Crawlino definitions files must have "
                                  "a non-empty 'crawler' section")

    # --------------------------------------------------------------------------
    # Map && init first level config
    # --------------------------------------------------------------------------
    return_obj.logName = gt(config_obj, "logName", "crawlino")

    # -------------------------------------------------------------------------
    # Load Model details
    # -------------------------------------------------------------------------
    return_obj.models = _parse_model_definitions(gt(config_obj,
                                                         "models",
                                                         []))

    # -------------------------------------------------------------------------
    # Load Crawler details
    # -------------------------------------------------------------------------
    return_obj.crawlers = _parse_crawlers_definitions(gt(config_obj,
                                                              "models",
                                                              []))

    # -------------------------------------------------------------------------
    # Coherence checks
    # -------------------------------------------------------------------------

    # Try to find main crawler. The start point. If we haven't found any start
    # point, then raise an exception
    if not any(gt(x, "mainCrawler", False) for x in return_obj.crawlers):
        raise CrawlinoMainCrawlerNotFound(
            "Unable to employ_name2employ_code the main Crawler in"
            "your crawler list. Please ensure you have set the property "
            "'mainCrawler' to one (and only one) crawler.")

    # Check that there's only one main crawler
    if sum([
        1 for x in return_obj.crawlers
            if gt(x, "mainCrawler", False) is True]) != 1:

        raise CrawlinoMainCrawlerDuplicated(
            "Only one crawlers must be set as a mainCrawler. Review your "
            "'mainCrawler' property in  your crawlers and ensure that only "
            "one have setted the property to 'true'")

    # Check that any crawler field has a map with the model
    _available_models = set(gt(x, "name") for x in return_obj.models)
    _crawler_models = set(gt(x, "modelMap") for x in return_obj.crawlers)

    if _crawler_models.difference(_available_models):
        log.error("Some crawler have 'modelMap' that has not defined into "
                  "models. Please create models before use it into "
                  "crawlers. These modelMaps needs to be defined into "
                  "models: {}".format(_crawler_models.difference(
            _available_models)))

    return return_obj


# --------------------------------------------------------------------------
# Configuration loaders
# --------------------------------------------------------------------------
def _load_from_json_file(json_path: str) -> Namespace:

    json_data = json.load(open(json_path),
                          object_hook=lambda d: Namespace(**d))

    return _parse_crawlino_definition(json_data)


def load_definition(path: str, config_type: str = "json") -> Namespace:
    """
    :param path: configuration file path
    :param config_type: format of input configuration file. Allowed values:
           "json"
    :return:
    """
    if config_type not in ALLOWED_CONFIGURATION_FILES_FORMAT:
        raise CrawlinoValueError(
            "Invalid Crawlino file definition in '{}'. Allowed "
            "values are: {}".format(
                path,
                ", ".join(ALLOWED_CONFIGURATION_FILES_FORMAT)
            ))

    if config_type == "json":
        return _load_from_json_file(path)


__all__ = ("load_definition",)
