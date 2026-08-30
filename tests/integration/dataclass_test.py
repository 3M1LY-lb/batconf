from unittest import TestCase

import batconf.sources.dataclass as dataclass_module


class DataclassConfigDeprecationTests(TestCase):
    """DataclassConfig is obsolete: Configuration reads schema defaults."""

    def test___getattr__(t):
        with t.subTest('warns and advises deletion'):
            with t.assertWarns(DeprecationWarning) as cm:
                alias = dataclass_module.__getattr__('DataclassConfig')
            t.assertEqual(
                "'DataclassConfig' is deprecated and will be removed in "
                'v0.5.0; Configuration reads schema defaults directly since '
                'v0.2.0, so a DataclassConfig(config_class) entry in a '
                'source list can be deleted.',
                str(cm.warning),
            )

        with t.subTest('resolves to the class'):
            t.assertIs(alias, dataclass_module._DataclassConfig)
