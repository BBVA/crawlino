Web plugin
==========

This plugin makes HTTP connection to a target

Quick start
-----------

blah

Requisites
----------

blah

YAML config
-----------

Json format example:

.. code-block:: yaml

    type: web
    config:
        httpMethod: GET
        contentType: json
        timeout: 0.8
        httpHeaders:
          header1: value1
          header2: value2
        data: {"hello": "world"}

Simple POST:

.. code-block:: yaml

    type: web
    config:
        httpMethod: POST
        data: id=1&user=root

GET with parameters in URL:

.. code-block:: yaml

    type: web
    config:
        httpMethod: POST
        url: /?id=1&user=root

You can omit some fields:

.. code-block:: yaml

    type: web
    config:
        httpMethod: POST


Even you can omit all the parameters, in this case a simple GET HTTP will be used:


.. code-block:: yaml

    type: web


Input data
----------

The plugin can accept any input with sources:

- url
- domain
- web

Output data
-----------

The plugin return a JSON as format:

.. code-block:: javascript

    {
      "status_code": 404,
      "headers": {
        "Content-Type": "text/html; charset=utf-8",
        "Content-Length": "29",
        "Server": "Werkzeug/0.14.1 Python/3.6.1",
        "Date": "Thu, 01 Mar 2018 09:44:20 GMT"
      },
      "content": "Not found data for this value"
      "request": {
        'method': 'post',
        'url': 'http://127.0.0.1:11000/user/auth',
        'headers': {
            'Content-Type': 'application/json'
        },
        'data': '{"user": "admin", "password": "batman"}'
        }
      }
    }


Examples
--------

blah