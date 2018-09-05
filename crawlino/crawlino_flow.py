STEP_CONFIG = "config"
STEP_SOURCES = "sources"
STEP_INPUT = "input"
STEP_EXTRACTOR = "extractors"
STEP_MODEL = "model"
STEP_HOOKS = "hooks"

RESULT_IS_MANDATORY = {
    STEP_CONFIG: False,
    STEP_SOURCES: True,
    STEP_INPUT: True,
    STEP_EXTRACTOR: True,
    STEP_MODEL: False,
    STEP_HOOKS: False
}

MAP_NEXT_STEP = {
    STEP_INPUT: (STEP_EXTRACTOR, STEP_MODEL, STEP_HOOKS),
    STEP_EXTRACTOR: (STEP_MODEL, STEP_HOOKS),
    STEP_MODEL: (STEP_HOOKS,),
    STEP_HOOKS: ()
}


def get_next_step_for_crawler(crawler_name: str) -> str:

    pass