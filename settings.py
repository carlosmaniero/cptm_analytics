"""
------------------------------------------------------------------------------
Settings from the project
------------------------------------------------------------------------------

To override the settings, set an environment variable with the
prefix "TORNADO_".

See the  core.conf module from more information.
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
data_workers = 1

# Intervals
crawler_download_data_interval = 0.5


if __name__ == '__main__':
    import pprint as pprint
    from core.conf import parse_settings

    __dict__ = parse_settings()
    pprint.pprint(__dict__)
