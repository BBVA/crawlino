import datetime

from typing import Union

import html2text
import markdown2
from lxml.html.clean import Cleaner


def camelcase2underscore(camel_case_name: str) -> str:
    _r = []

    _pre_space = False
    for i in range(len(camel_case_name)):
        _pos = camel_case_name[i]

        if _pos.islower():
            if _pre_space:
                _r.append("_")

            _r.append(_pos)
            _pre_space = False

        elif _pos == " ":
            _pre_space = True
            continue
        else:

            _r.append("_")
            _r.append(_pos.lower())
            _pre_space = False

    ret = "".join(_r)

    if ret.startswith("_"):
        ret = ret[1:]
    if ret.endswith("_"):
        ret = ret[:-1]

    return ret


# --------------------------------------------------------------------------
# HTML transformations
# --------------------------------------------------------------------------
def html2simple_html(html_text: str):
    description_markdown = html2plain_text(html_text)
    clean_html = markdown2.markdown(description_markdown)

    cleaner = Cleaner(page_structure=True,
                      meta=False,
                      embedded=True,
                      links=True,
                      style=False,
                      processing_instructions=True,
                      inline_style=True,
                      scripts=False,
                      javascript=False,
                      comments=False,
                      frames=False,
                      forms=False,
                      annoying_tags=True,
                      remove_unknown_tags=True,
                      safe_attrs_only=True,
                      safe_attrs=frozenset(
                          ['src', 'href', 'title', 'name',
                           'id']),
                      remove_tags=('span', 'font', 'div'))

    return cleaner.clean_html(clean_html)


def html2plain_text(html_text: str):
    o = html2text.HTML2Text()
    o.ignore_images = True
    o.body_width = 1000000

    # HTML -> Markdown
    description_markdown = o.handle(html_text)

    # From uppercase letter with tildes -> lowercase tiles
    description_markdown = description_markdown.replace("Á", "á")\
        .replace("É", "é").replace("Í", "í")\
        .replace("Ó", "ó").replace("Ú", "ú")

    return description_markdown


def auto_setter(content_type: str) -> Union[datetime.datetime, int, str]:

    auto_setters = {
        "text": lambda: "",
        "datetime": lambda: datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat(),
        "number": lambda: 1,
        "link": lambda: "",
    }

    return auto_setters[content_type]()


__all__ = ("camelcase2underscore", "html2plain_text", "html2simple_html",
           "html2text")
