from unittest import TestCase

import batconf.sources.dataclass as dataclass_module


class DataclassConfigDeprecationTests(TestCase):
    """DataclassConfig is obsolete: Configuration reads schema defaults."""

    def test_access_fires_warning(t):
        with t.assertWarns(DeprecationWarning) as cm:
            dataclass_module.__getattr__('DataclassConfig')
        t.assertEqual(
            "'DataclassConfig' is deprecated and will be removed in "
            'v0.5.0; Configuration reads schema defaults directly since '
            'v0.2.0, so a DataclassConfig(config_class) entry in a source '
            'list can be deleted.',
            str(cm.warning),
        )

    def test_resolves_to_the_class(t):
        with t.assertWarns(DeprecationWarning):
            alias = dataclass_module.__getattr__('DataclassConfig')
        t.assertIs(alias, dataclass_module._DataclassConfig)
