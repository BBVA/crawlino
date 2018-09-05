from typing import Dict

from crawlino.crawlino_flow import STEP_SOURCES
from crawlino.exceptions import CrawlinoValueError
from crawlino.models import CModelBase, CModelBaseLoader
from crawlino.modules_stores import CrawlinoModulesStore


class CMSource(CModelBase, metaclass=CModelBaseLoader):

    __slots__ = ("type", "config", "name")

    def __init__(self, type: str, config: Dict, name: str = None):
        self.type = type
        self.name = name or ""
        self.config = config

        if not self.type:
            raise CrawlinoValueError("Source must has the 'type' property")

        if self.config is None:
            raise CrawlinoValueError("Source must has a 'config' property")

        if CrawlinoModulesStore.find_module(STEP_SOURCES, self.type) is None:
            raise CrawlinoValueError("Invalid 'type' property value",
                                     exc_info=True,
                                     extra={
                                         "given_source_type": self.type
                                     })

    @property
    def to_dict(self):
        return {
            "type": self.type,
            "config": self.config,
            "name": self.name
        }

    @property
    def module_name(self) -> str:
        return "sources"


__all__ = ("CMSource", )
