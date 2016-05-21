"""
------------------------------------------------------------------------------
APP CONF
------------------------------------------------------------------------------
This module have utils methods about settings manager.
"""
import os


def parse_settings():
    """
    The parse_settings method get variable from the enviroment with the
    prefix TORNADO_

    usage:
        Run this, before the app loader.

        >>> from core.conf import parse_settings
        >>> if __name__ == '__main__':
        >>>     parse_settings()

    example:
        # Show default settings:
        $ python settings.py
        {'cptm_url': 'http://cptm.sp.gov.br/',
         'crawler_workers': 2,
         'database_name': 'cptm',
         'debug': True,
         'port': 8000}

        # Export a environ variable:
        $ export TORNADO_PORT=8080

        # Check from settings again:
        $ python settings.py
        {'cptm_url': 'http://cptm.sp.gov.br/',
         'crawler_workers': 2,
         'database_name': 'cptm',
         'debug': True,
         'port': 8080}

    """
    import settings
    __dict__ = {}
    for key in dir(settings):
        value = getattr(settings, key)

        if not key.startswith('_'):
            value_type = type(value)
            environ_key = 'TORNADO_{}'.format(key.upper())
            value = os.environ.get(environ_key, value)
            # Cast Info
            __dict__[key] = value_type(value)
            setattr(settings, key, __dict__[key])

    return __dict__
