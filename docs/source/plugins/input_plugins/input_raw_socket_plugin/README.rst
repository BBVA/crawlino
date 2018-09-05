Raw socket plugin
=================

This plugin makes raw socket connections to a target

YAML config
-----------

YAML format example:

.. code-block:: yaml

      type: raw_socket
      config:
        port: 8080
        proto: tcp
        timeout: 0.05
        data: "GET / HTTP/1.1\r\n\r\n"

All the options are optional except 'port'

.. code-block:: yaml

      type: raw_socket
      config:
        port: $generator(numeric, 9990, 10001)

Available values in 'proto' are:

- tcp
- udp

If you don't specify 'data' value, plugin with send a CRLF value: "\r\n\r\n"


Input data
----------

The plugin can accept any input with sources:

- ip
- domain
- web
- url

Output data
-----------

The plugin return a JSON as format:

.. code-block:: yaml

    {
        "host": "127.0.0.1",
        "data": null,
        "port": "9995",
        "status": "closed/filtered"
    }

Available values for 'port' are:

- open
- closed/filtered
