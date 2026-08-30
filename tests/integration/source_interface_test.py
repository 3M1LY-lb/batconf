from unittest import TestCase

import batconf.source as source_module


class SourceInterfaceDeprecationTests(TestCase):
    """SourceInterfaceP is the extension point; the ABC is legacy."""

    def test_access_fires_warning(t):
        with t.assertWarns(DeprecationWarning) as cm:
            source_module.__getattr__('SourceInterface')
        t.assertEqual(
            "'SourceInterface' is deprecated and will be removed in "
            "v0.5.0; use 'SourceInterfaceP' instead.",
            str(cm.warning),
        )

    def test_resolves_to_the_abc(t):
        with t.assertWarns(DeprecationWarning):
            alias = source_module.__getattr__('SourceInterface')
        t.assertIs(alias, source_module._SourceInterface)

    def test_unknown_name_raises_attribute_error(t):
        with t.assertRaises(AttributeError) as err:
            source_module.__getattr__('NoSuchName')
        t.assertEqual(
            "module 'batconf.source' has no attribute 'NoSuchName'",
            str(err.exception),
        )
