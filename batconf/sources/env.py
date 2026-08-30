import os

from .types import SourceInterfaceP
from ._compat import deprecated_module, make_deprecated_getattr


class EnvSource(SourceInterfaceP):
    """Configuration source that reads from environment variables.

    Keys are resolved by converting the dotted config path into an
    upper-case, underscore-separated environment variable name.
    For example, ``project.database.host`` becomes
    ``PROJECT_DATABASE_HOST``.  When no path is provided the prefix
    ``BAT`` is used instead.

    Examples
    --------
    >>> import os
    >>> os.environ['PROJECT_DATABASE_HOST'] = 'localhost'
    >>> src = EnvSource()
    >>> src.get(key='host', path='project.database')
    'localhost'
    """

    def __init__(self) -> None:
        pass

    def get(
        self,
        key: str,
        path: str | None = None,
        module: str | None = None,
    ) -> str | None:
        path = deprecated_module(path, module)
        return os.getenv(self.env_name(key, path))

    def env_name(self, key: str, module: str | None = None) -> str:
        if module:
            path = module.split('.') + key.split('.')
        else:
            path = ['BAT'] + key.split('.')

        return '_'.join(path).upper()

    def __str__(self):
        return f'Environment Variables: {repr(self)}'

    def __repr__(self):
        return f'{self.__class__.__name__}()'


__getattr__ = make_deprecated_getattr(
    deprecated={'EnvConfig': 'EnvSource'},
    module_globals=globals(),
    module_name=__name__,
)
