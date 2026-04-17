__version__ = '0.0.18'

# messytables 0.15.2 is unmaintained and uses `from collections import Mapping`
# which was removed in Python 3.10 (moved to collections.abc). Since upgrading
# messytables is not an option, we restore the old attributes before it imports.
import sys
if sys.version_info >= (3, 3):
    import collections.abc
    if not hasattr(collections, 'Mapping'):
        collections.Mapping = collections.abc.Mapping
    if not hasattr(collections, 'MutableMapping'):
        collections.MutableMapping = collections.abc.MutableMapping
    import collections
