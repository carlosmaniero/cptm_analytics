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

# Http Settings
port = 8000

# Database settings
database_name = 'cptm'

# CPTM Info
cptm_url = 'http://cptm.sp.gov.br/'

# Development Settings
debug = True

# Workers
crawler_workers = 2
crawler_data_workers = 1

# Intervals
crawler_download_data_interval = 0.5


if __name__ == '__main__':
    import pprint as pprint
    from core.conf import parse_settings

    __dict__ = parse_settings()
    pprint.pprint(__dict__)
