Environment configuration
=========================

Accessing global config
-----------------------

*Crawlino* has a special global object that stores all the global config. This object is **read-only** for the plugins, and only *configuration plugins* can store information on it.

.. code-block:: python

    from crawlino import current_config

    print(current_config.running_options.verbosity)

