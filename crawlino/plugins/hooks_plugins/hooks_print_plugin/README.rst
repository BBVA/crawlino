Print plugin
============

This plugin display in the screen received results

YAML config
-----------

Json format example:

.. code-block:: json

    -   type: print
        config:
          format: csv

Available values for 'format' are:

- json
- csv

if you don't specify config values, default format are 'json'.

