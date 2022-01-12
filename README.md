# cerberus-kind
Help to select a schema by "kind" key on cerberus.

[![Upload Python Package](https://github.com/onetop21/cerberus-kind/actions/workflows/python-publish.yml/badge.svg)](https://github.com/onetop21/cerberus-kind/actions/workflows/python-publish.yml)

## Installation
```bash
$ pip install cerberus-kind
```

## How to Use
```python
from cerberus_kind import Validator

schema = {
    'item_default': {
        'schema': {
            'data': {
                'type': 'string', 
                'default': 'Hello World'
            }
        },
        'default': {}
    },
    'item_selector': {
        'selector': {
            'kind_string': {
                'data': {
                    'type': 'string',
                    'default': 'Hello Selector'
                }
            },
            'kind_integer': {
                'data': {
                    'type': 'integer',
                    'default': 12345
                }
            },
            'kind_list': {
                'data': {
                    'type': 'list',
                    'schema': {
                        'type': 'string',
                        'schema': {
                            'type': 'string'
                        },
                        'default': ['A', 'B', 'C']
                    }
                }
            }
        }
    }
}

document = {
    'item_selector': {
        'kind': 'Kind_String'
    }
}

v = Validator(schema)
if v.validate(document):
    print("[Verified]")
    pprint(v.normalized(document), sort_dicts=False)
else:
    print("[Errors]", v.errors)
    sys.exit(1)

# RESULT
'''
[Verified]
{'item_selector': {'kind': 'Kind_String', 'data': 'Hello Selector'},
 'item_default': {'data': 'Hello World'}}
'''

# Support sort items by schema.
schema = {
    ...
    'schema': {
        'order': 1,
        ...
    }
    ...
}
...
v.normalized_by_order(document)

# Support selector schema on root.
schema = {
    '__root__': {
        'selector': {
            ...
        }
    }
}

```
  
