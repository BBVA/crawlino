Print plugin
============

This plugin send emails when step before was get results.

YAML config
-----------

Fields mandatory are:

- from
- to
- subjectField
- server.user
- server.password


Json extended format
++++++++++++++++++++

.. code-block:: yaml

  - type: mail
    config:
      from: from@mail.com
      to: to@mail.com
      subject: My custom subject
      bodyField: status
      server:
        smtp: smtp.gmail.com
        user: $MAIL_USER$
        password: $MAIL_PASSWORD$
        port: 587
        tls: True


Fields explanation:

- **bodyField**: field got from previous step result
- **subject**: got the first 100 characters from previous bodyField if empty


Json quick format
+++++++++++++++++

.. code-block:: yaml

  - type: mail
    config:
      from: from@gmail.com
      to: to@gmail.com
      body: status
      server:
        user: $MAIL_USER$
        password: $MAIL_PASSWORD$


If a **gmail address** is detected, plugin will resolver smtp server, tls and port.