from unittest import TestCase

import batconf.sources.env as env_module


class EnvConfigDeprecationTests(TestCase):
    """EnvConfig is the pre-0.4 name for EnvSource."""

    def test_access_fires_warning(t):
        with t.assertWarns(DeprecationWarning) as cm:
            env_module.__getattr__('EnvConfig')
        t.assertEqual(
            "'EnvConfig' is deprecated and will be removed in v0.5.0; "
            "use 'EnvSource' instead.",
            str(cm.warning),
        )

    def test_resolves_to_the_renamed_class(t):
        with t.assertWarns(DeprecationWarning):
            alias = env_module.__getattr__('EnvConfig')
        t.assertIs(alias, env_module.EnvSource)
