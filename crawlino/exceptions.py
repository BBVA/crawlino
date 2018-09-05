class CrawlinoException(Exception):
    def __init__(self, message: str, **kwargs):
        self.message = message
        self.extra = kwargs


class CrawlinoValueError(CrawlinoException):
    pass


class CrawlinoStepException(CrawlinoException):
    pass


class CrawlinoNotFoundError(CrawlinoException):
    pass


class CrawlinoFormatError(CrawlinoException):
    pass


class CrawlinoMainCrawlerNotFound(CrawlinoException):
    pass


class CrawlinoModelsNotFound(CrawlinoException):
    pass


class CrawlinoMainCrawlerDuplicated(CrawlinoException):
    pass
