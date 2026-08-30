"""Verify the public batconf.sources.types namespace."""
import warnings
from unittest import TestCase

from .. import types


class SourcesTypesTests(TestCase):
    """Verify all intended symbols are importable from batconf.sources.types."""

    def test_type_aliases(t):
        t.assertTrue(hasattr(types, 'ConfigFileFormats'))
        t.assertTrue(hasattr(types, 'MissingFileOption'))

    def test_protocols(t):
        t.assertTrue(hasattr(types, 'SourceInterfaceP'))
        t.assertTrue(hasattr(types, 'FileSourceP'))

    def test_runtime_checkable(t):
        """The protocols answer isinstance, so a custom source can be
        checked without inheriting from anything."""

        class Source:
            def get(self, key: str, path: str | None = None) -> None: ...

        with t.subTest('SourceInterfaceP instance'):
            t.assertIsInstance(Source(), types.SourceInterfaceP)

        with t.subTest('SourceInterfaceP subclass'):
            t.assertTrue(issubclass(Source, types.SourceInterfaceP))

        with t.subTest('FileSourceP instance'):
            t.assertIsInstance(Source(), types.FileSourceP)

    def test_deprecated_names(t):
        """Old Proto-suffixed names emit DeprecationWarning but still resolve."""
        with t.subTest('SourceInterfaceProto'):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter('always')
                alias = types.SourceInterfaceProto
            t.assertIs(alias, types.SourceInterfaceP)
            t.assertEqual(len(w), 1)
            t.assertEqual(
                "'SourceInterfaceProto' is deprecated and will be removed "
                "in v0.5.0; use 'SourceInterfaceP' instead.",
                str(w[0].message),
            )
            t.assertIs(w[0].category, DeprecationWarning)

    def test_all_is_complete(t):
        """Every symbol in __all__ must be importable from batconf.sources.types."""
        for name in types.__all__:
            t.assertTrue(
                hasattr(types, name),
                msg=f'batconf.sources.types.__all__ lists {name!r} but it is not importable',
            )
