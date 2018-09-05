Print plugin
============

This plugin display in the screen received results

YAML config
-----------

YAML format example:

.. code-block:: yaml

    -   type: print
        config:
          format: csv

Available values for 'format' are:

- json
- csv

if you don't specify config values, default format are 'json'.

