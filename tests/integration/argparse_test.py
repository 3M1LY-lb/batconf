from unittest import TestCase

import batconf.sources.argparse as argparse_module
from batconf.sources.argparse import NamespaceSource

from argparse import ArgumentParser, Namespace


def argparser(cfg_path='root'):
    p = ArgumentParser()
    p.add_argument('-a', dest=f'{cfg_path}.alpha')

    commands = p.add_subparsers(dest='command')
    commands.add_parser(
        'command1',
        parents=[command_cli(f'{cfg_path}.command1')],
        add_help=False,
    )
    # reusable sub-parser for commands
    commands.add_parser(
        'command2',
        parents=[command_cli(f'{cfg_path}.command2')],
        add_help=False,
    )

    return p


def command_cli(cfg_path: str):
    p = ArgumentParser()
    p.add_argument('--cmd-option', dest=f'{cfg_path}.opt')
    return p


class NamespaceSourceTests(TestCase):
    def test_(t) -> None:
        parser = argparser()
        args = ['-a=value_a', 'command1', '--cmd-option=co1']
        namespace: Namespace = parser.parse_args(args)  # , NestedNameSpace())
        # check access to path.like attributes on the Namespace
        t.assertEqual(getattr(namespace, 'root.alpha'), 'value_a')
        t.assertEqual(getattr(namespace, 'root.command1.opt'), 'co1')

        # Create a Configuration Source from an argparse Namespace
        src = NamespaceSource(namespace)
        t.assertEqual(src.get('root.alpha'), 'value_a')
        t.assertEqual(src.get('root.command1.opt'), 'co1')
        t.assertIsNone(src.get('root.command2.opt'))

        # Example using command2
        args = ['command2', '--cmd-option=co2']
        parser = argparser()
        namespace = parser.parse_args(args)
        src = NamespaceSource(namespace)
        t.assertIsNone(src.get('root.command1.opt'))
        t.assertEqual(src.get('root.command2.opt'), 'co2')


class NamespaceConfigDeprecationTests(TestCase):
    """NamespaceConfig is the pre-0.4 name for NamespaceSource."""

    def test___getattr__(t):
        with t.subTest('warns and names the replacement'):
            with t.assertWarns(DeprecationWarning) as cm:
                alias = argparse_module.__getattr__('NamespaceConfig')
            t.assertEqual(
                "'NamespaceConfig' is deprecated and will be removed in "
                "v0.5.0; use 'NamespaceSource' instead.",
                str(cm.warning),
            )

        with t.subTest('resolves to the renamed class'):
            t.assertIs(alias, argparse_module.NamespaceSource)
