import os


def parse_settings():
    import settings
    __dict__ = {}
    for key in dir(settings):
        value = getattr(settings, key)

        if not key.startswith('_'):
            value_type = type(value)
            environ_key = 'CPTM_{}'.format(key.upper())
            value = os.environ.get(environ_key, value)
            # Cast Info
            __dict__[key] = value_type(value)
            setattr(settings, key, __dict__[key])

    from core.database import get_database
    settings.db = __dict__['db'] = get_database()
    return __dict__
