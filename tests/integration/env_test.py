from unittest import TestCase

import batconf.sources.env as env_module


class EnvConfigDeprecationTests(TestCase):
    """EnvConfig is the pre-0.4 name for EnvSource."""

    def test___getattr__(t):
        with t.subTest('warns and names the replacement'):
            with t.assertWarns(DeprecationWarning) as cm:
                alias = env_module.__getattr__('EnvConfig')
            t.assertEqual(
                "'EnvConfig' is deprecated and will be removed in v0.5.0; "
                "use 'EnvSource' instead.",
                str(cm.warning),
            )

        with t.subTest('resolves to the renamed class'):
            t.assertIs(alias, env_module.EnvSource)
