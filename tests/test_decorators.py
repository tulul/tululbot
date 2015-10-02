from unittest.mock import Mock, patch

import pytest

from tululbot.decorators import CommandDispatcher, CommandNotFoundError


def test_no_matching_command():
    dispatcher = CommandDispatcher()
    mock_callback = Mock()

    dispatcher.add_command(r'^/hello$', mock_callback)
    with pytest.raises(CommandNotFoundError):
        dispatcher.run_command('/world')

    assert not mock_callback.called


def test_run_command_returns_the_same_value_as_callback():
    dispatcher = CommandDispatcher()
    mock_callback = Mock()
    mock_callback.return_value = 'foo bar'

    dispatcher.add_command(r'^/hello$', mock_callback)
    rv = dispatcher.run_command('/hello')
    assert rv == 'foo bar'


def test_callback_is_called_with_regex_params():
    dispatcher = CommandDispatcher()
    mock_callback = Mock()

    dispatcher.add_command(r'^/hello (\w+) (\w+)$', mock_callback)
    dispatcher.run_command('/hello foo bar')
    mock_callback.assert_called_once_with('foo', 'bar')


def test_multiple_commands():
    dispatcher = CommandDispatcher()
    mock_callback1 = Mock()
    mock_callback2 = Mock()

    dispatcher.add_command(r'^/hello$', mock_callback1)
    dispatcher.add_command(r'^/world$', mock_callback2)
    dispatcher.run_command('/world')
    assert not mock_callback1.called
    assert mock_callback2.called


def test_multiple_matching_commands():
    dispatcher = CommandDispatcher()
    mock_callback1 = Mock()
    mock_callback2 = Mock()

    dispatcher.add_command(r'^/hello$', mock_callback1)
    dispatcher.add_command(r'^/hello$', mock_callback2)
    dispatcher.run_command('/hello')
    assert not mock_callback2.called
    assert mock_callback1.called


def test_command_decorator_with_no_params():
    dispatcher = CommandDispatcher()
    with patch.object(dispatcher, 'add_command') as mock_add_cmd:
        pattern = r'^/hello$'

        @dispatcher.command(pattern)
        def hello():
            return 'Hello world!'

        mock_add_cmd.assert_called_once_with(pattern, hello)


def test_command_decorator_with_params():
    dispatcher = CommandDispatcher()
    with patch.object(dispatcher, 'add_command') as mock_add_cmd:
        pattern = r'^/hello (?P<name>\w+)$'

        @dispatcher.command(pattern)
        def greet(name):
            return 'Hello {}!'.format(name)

        mock_add_cmd.assert_called_once_with(pattern, greet)
