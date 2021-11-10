# Test application
import sys
from cerberus_kind import Validator
if sys.version_info.major >= 3 and sys.version_info.minor >= 8:
    from pprint import pprint
else:
    def pprint(doc, sort_dicts=False):
        if sort_dicts:
            from pprint import pprint
            pprint(doc)
        else:
            import json
            print(json.dumps(doc, indent=2))

schema = {
    '__root__': {
        'type': 'dict',
        'selector': {
            'project': {
                'name': {
                    'type': 'string',
                    'required': True,
                    'empty': False,
                    'description': 'Hello World',
                    'order': 1},
                'version': {
                    'type': 'string',
                    'regex': '[0-9]+\\.[0-9]+\\.[0-9]+',
                    'default': '0.0.1',
                    'order': 2},
                'workspace': {
                    'type': 'dict',
                    'selector': {
                        'workspace': {
                            'base': {
                                'type': 'string',
                                'regex': '(?:.+/)?([^:]+)(?::.+)?',
                                'required': True},
                            'command': {
                                'type': ['string', 'list']}},
                        'buildscript': {
                            'buildscript': {
                                'type': 'string',
                                'default': 'FROM    python:latest',
                                'required': True},
                            'ignores': {
                                'type': 'list',
                                'default': ['**/.*'],
                                'schema': {'type': 'string'}}},
                        'dockerfile': {
                            'filePath': {
                                'type': 'string',
                                'default': 'Dockerfile',
                                'required': True},
                            'ignorePath': {
                                'type': 'string',
                                'default': '.dockerignore'}}},
                    'order': 10},
                'app': {
                    'type': 'dict',
                    'valuesrules': {
                        'type': 'dict',
                        'selector': {
                            'job': {
                                'command': {'type': ['string',
                                            'list']},
                                'restartPolicy': {'type': 'string',
                                                'allowed': ['never',
                                                            'onFailure'],
                                                'default': 'never',
                                                'excludes': 'runSpec'}},
                            'service': {
                                'command': {'type': ['string',
                                            'list']},
                                'restartPolicy': {'type': 'string',
                                                'allowed': ['always'],
                                                'default': 'always',
                                                'excludes': 'runSpec'}}}},
                    'order': 30}}}}}
document = {'name': 'Your Project',
            'kind': 'Project',
            'workspace': {'kind': 'Dockerfile', 'filePath': '.'},
            'app': {
                'server': {
                    'kind': 'Service',
                    'command': 'python server.py'
                    },
                'client': {
                    'kind': 'Job',
                    'command': 'python client.py'}}}

class ValidatorImpl(Validator):
    def _validate_description(self, constraint, field, value):
        '''For use YAML Editor'''

if __name__ == '__main__':
    print("* Schema *")
    pprint(schema, sort_dicts=False)
    print("* Document *")
    pprint(document, sort_dicts=False)
    v = ValidatorImpl(schema)
    if v.validate(document):
        print("[Verified]")
        pprint(v.normalized_by_order(document), sort_dicts=False)
    else:
        print("[Errors]", v.errors)
        sys.exit(1)
