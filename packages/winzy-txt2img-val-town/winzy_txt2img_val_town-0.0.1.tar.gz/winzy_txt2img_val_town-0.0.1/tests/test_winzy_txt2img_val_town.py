import pytest
import winzy_txt2img_val_town as w

from argparse import Namespace, ArgumentParser

def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_args(['hello'])
    assert result.text == ["hello"]
    assert result.save is False
    assert result.hd is False


def test_plugin(capsys):
    w.t2i_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``winzy`` plugin." in captured.out
