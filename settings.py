"""
------------------------------------------------------------------------------
Settings from the project
------------------------------------------------------------------------------

To override the settings, set an environment variable with the prefix "CPTM_".

usage:
    # Show default settings:
    $ python settings.py
    {'cptm_url': 'http://cptm.sp.gov.br/',
     'crawler_workers': 2,
     'database_name': 'cptm',
     'debug': True,
     'port': 8000}

    # Export a environ variable:
    $ export CPTM_PORT=8080

    # Check from settings again:
    $ python settings.py
    {'cptm_url': 'http://cptm.sp.gov.br/',
     'crawler_workers': 2,
     'database_name': 'cptm',
     'debug': True,
     'port': 8080}

"""
import os as _os
import pprint as _pprint

# Http Settings
port = 8000

# Database settings
database_name = 'cptm'

# Development Settings
debug = True
crawler_workers = 2
cptm_url = 'http://cptm.sp.gov.br/'


def _parse_settings():
    settings = globals()
    __dict__ = {}
    for key, value in settings.items():
        if not key.startswith('_'):
            value_type = type(value)
            environ_key = 'CPTM_{}'.format(key.upper())
            value = _os.environ.get(environ_key, value)
            # Cast Info
            __dict__[key] = value_type(value)
    return __dict__

__dict__ = _parse_settings()


if __name__ == '__main__':
    _pprint.pprint(__dict__)
