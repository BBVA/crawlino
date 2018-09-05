Under the hoods
===============

How Crawlino works?
-------------------

Modules available:

#. Sources modules
#. Input Module
#. Model modules
#. Extractors modules
#. Hooks Modules


What modules are mandatory to specify in the JSON / YAML file?
--------------------------------------------------------------

Apart of Crawler it self info (::samp:`config` section) the crawler definition must have these other sections:

#. sources
#. input
#. model

Feedback model for the plugins
------------------------------

- Sources returns a List of objects
- Inputs return a single object.
- Extractors return a single object
- Model return a single object
- Hooks doesn't return nothing

Execution model
---------------

The execution, in pseudo-code is like that:

.. code-block:: modula2

    FOR EACH [$source in sources] DO

        $RESULT := $source -> Input -> Extractor -> Model

        FOR EACH [$Hook in $CRAWLER_HOOKS] DO
            EXECUTE $hook <- $RESULT
        DONE

    DONE

