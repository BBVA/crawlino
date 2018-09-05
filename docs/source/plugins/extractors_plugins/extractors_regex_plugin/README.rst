Regex plugin
============


YAML Format


.. code-block:: yaml

    extractors:
      - ruleSet:
          name: rule1
          description: do simple xpath search
          mapTo: myVar
          exitOnMatch: true
          inputVar: status
          report: original
          rules:
            - type: regex
              config:
                order: 1
                reportGroup: 2
                expressions:
                  - >
                    (closed/)([\w]+)

            - type: regex
              config:
                order: 2
                expressions:
                  - "open"


Options
-------

**report**

Allowed values:

- original: return the original input data from previous step
- group: return only returned value from regex group
- [TEXT]: this text is a index in the previous data. For example: Maybe we would want to detect that an port is open, but returned the web server banner

Default value is: *group*