import pytest
import winzy_weather as w

from argparse import  ArgumentParser

def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_args([])
    assert result.city is None
    assert result.wide == False
    assert result.no_forecast == False
    assert result.today == False
    assert result.full == False



def test_plugin(capsys):
    w.weather_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``winzy`` plugin." in captured.out
