Crawler Config Section
======================

These king of plugins stores their results in the ::samp:`current_config` object.

**Basic format in the config file**

Example:

.. code-block:: yaml

    config:
      logger: crawlino
        logLevel: 2
      logger: myCustomlogger
        logLevel: 5

Parameters
----------

logger
++++++

**Description**

This parameters specify an additional logger for this crawler. By default, *Crawlino* uses the crawler with name *crawlino*, but if you want, you can specify another.

You could want to specify another to use other log lever or to send log data to a different place than the general logger.

**type and allowed values**

string

logLevel
++++++++

**Description**

Set log level for an specific log.

**type and allowed values**

- type: int
- allowed values: 0 - 5

