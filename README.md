# cerberus-kind
Help to select a schema by "kind" key on cerberus.

## Installation
```bash
$ pip install cerberus_kind
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
  
### Callback customize
#### return False
> Escape 'with statement' forcley.
#### return True
> Switch 'interrupted flag'.
``` python
def callback():
  print('Interrupted by User.')
  return False
  
with InterruptHandler(callback) as h:
  ...
```

## Example
```python
import time
from interrupt_handler import InterruptHandler, default_callback

if __name__ == '__main__':
    import time
    main_loop = True
    sub_loop = True
    with InterruptHandler(default_callback('Locked', True)) as h1:
        while not h1.interrupted:
            print(f'MainLoop {time.time()}, {h1}, {h1.interrupted}')
            with InterruptHandler(default_callback('Message2')) as h2:
                while sub_loop:
                    print(f'SubLoop {time.time()}')
                    time.sleep(1)
            sub_loop = False
            time.sleep(1)
    main_loop = False
```

