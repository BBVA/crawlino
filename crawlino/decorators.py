"""
Part of this code was based on:

https://stackoverflow.com/a/653478

"""
from crawlino.crawlino_flow import *


def _decorates_function(f, name: str or None, module_type: str):
    if not name:
        name = f.__name__.replace(f"{module_type}_", "").\
            replace(f"{module_type[:-1]}_", "")

    f.crawlino_module_name = name
    f.crawlino_module_type = module_type
    return f


def input_plugin(fn=None, *, name: str = None):

    if fn is None:
        def decorator(fn):
            return _decorates_function(fn, name, STEP_INPUT)
        return decorator

    else:
        return _decorates_function(fn, None, STEP_INPUT)


def source_plugin(fn=None, *, name: str = None):

    if fn is None:
        def decorator(fn):
            return _decorates_function(fn, name, STEP_SOURCES)
        return decorator

    else:
        return _decorates_function(fn, None, STEP_SOURCES)


def hook_plugin(fn=None, *, name: str = None):

    if fn is None:
        def decorator(fn):
            return _decorates_function(fn, name, STEP_HOOKS)
        return decorator

    else:
        return _decorates_function(fn, None, STEP_HOOKS)


def config_plugin(fn=None, *, name: str = None):

    if fn is None:
        def decorator(fn):
            return _decorates_function(fn, name, STEP_CONFIG)
        return decorator

    else:
        return _decorates_function(fn, None, STEP_CONFIG)


def generator_plugin(fn=None, *, name: str = None):

    if fn is None:
        def decorator(fn):
            return _decorates_function(fn, name, "generators")
        return decorator

    else:
        return _decorates_function(fn, None, "generators")


def extractor_plugin(fn=None, *, name: str = None):

    if fn is None:
        def decorator(fn):
            return _decorates_function(fn, name, STEP_EXTRACTOR)
        return decorator

    else:
        return _decorates_function(fn, None, STEP_EXTRACTOR)


__all__ = ("input_plugin", "source_plugin", "extractor_plugin", "hook_plugin",
           "config_plugin", "generator_plugin")
