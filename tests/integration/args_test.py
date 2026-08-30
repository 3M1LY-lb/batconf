import warnings
from argparse import Namespace
from unittest import TestCase

import batconf.sources.args as args_module


class CliArgsConfigDeprecationTests(TestCase):
    """CliArgsConfig warns when the name is accessed, not when it is used."""

    def test_access_fires_warning(t):
        with t.assertWarns(DeprecationWarning) as cm:
            args_module.__getattr__('CliArgsConfig')
        t.assertEqual(
            "'CliArgsConfig' is deprecated and will be removed in v0.5.0; "
            "use 'NamespaceSource' instead.",
            str(cm.warning),
        )

    def test_instantiation_is_silent(t):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            args_module._CliArgsConfig(Namespace(key='value'))
        t.assertEqual([], w)
