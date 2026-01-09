__version__ = '0.0.18'

# Monkey patch for Python 3.10+ compatibility with messytables
import sys
if sys.version_info >= (3, 3):
    import collections.abc
    if not hasattr(collections, 'Mapping'):
        collections.Mapping = collections.abc.Mapping
    if not hasattr(collections, 'MutableMapping'):
        collections.MutableMapping = collections.abc.MutableMapping
    import collections
