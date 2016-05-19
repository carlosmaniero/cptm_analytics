import os as _os

# Http Settings
port = 8000

# Database settings
database_name = 'cptm'

# Development Settings
debug = True
crawler_workers = 2


def _parse_settings():
    settings = globals()
    for key, value in settings.items():
        if not key.startswith('_'):
            value_type = type(value)
            value = _os.environ.get('CPTM_{}'.format(key), value)
            # Cast Info
            settings[key] = value_type(value)
    return settings

__dict__ = _parse_settings()


if __name__ == '__main__':
    print(__dict__)
