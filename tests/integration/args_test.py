import warnings
from argparse import Namespace
from unittest import TestCase

import batconf.sources.args as args_module


class CliArgsConfigDeprecationTests(TestCase):
    """CliArgsConfig warns when the name is accessed, not when it is used."""

    def test___getattr__(t):
        with t.subTest('warns and names the replacement'):
            with t.assertWarns(DeprecationWarning) as cm:
                alias = args_module.__getattr__('CliArgsConfig')
            t.assertEqual(
                "'CliArgsConfig' is deprecated and will be removed in "
                "v0.5.0; use 'NamespaceSource' instead.",
                str(cm.warning),
            )

        with t.subTest('resolves to the legacy class'):
            t.assertIs(alias, args_module._CliArgsConfig)

    def test__CliArgsConfig(t):
        with t.subTest('construction emits no warning'):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter('always')
                args_module._CliArgsConfig(Namespace(key='value'))
            t.assertEqual([], w)
