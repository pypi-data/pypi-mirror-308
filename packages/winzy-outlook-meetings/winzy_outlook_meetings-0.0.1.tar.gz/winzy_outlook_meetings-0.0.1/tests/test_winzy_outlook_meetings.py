import pytest
import winzy_outlook_meetings as w
from datetime import datetime

from argparse import Namespace, ArgumentParser


def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    dateval = datetime.today().strftime("%Y-%m-%d")
    result = parser.parse_args(["-s", dateval])
    assert result.start == dateval
    assert result.days == 1


def test_plugin(capsys):
    w.outcal_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``winzy`` plugin." in captured.out
