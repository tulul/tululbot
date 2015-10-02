import re


class CommandNotFoundError(Exception):
    pass


class CommandDispatcher:
    """TululBot command dispatcher class."""

    def __init__(self):
        self._command_list = []

    def add_command(self, pattern, callback):
        """Register command and the corresponding callback.

        `pattern` is a Python regex pattern. It may contains a grouping pattern
        so that the callback will be called with those groups as its arguments
        if the command given to `run_command` matches the given `pattern`.
        For readability, it is recommended to use the named group pattern as shown
        in the example.

        Arguments:
        pattern -- Python regex pattern.
        callback -- Callback function to be called when the given command matches `pattern`.

        Example:
        >>> def greet(name):
        ...     print('Hello, {}!'.format(name))
        ...
        >>> dispatcher = CommandDispatcher()
        >>> dispatcher.add_command(r'^/hello (?P<name>\w+)$', greet)
        >>> dispatcher.run_command('/hello world')
        Hello, world!
        """
        self._command_list.append((re.compile(pattern), callback))

    def command(self, pattern):
        """Decorator to `add_command` method.

        This decorator is provided as syntactic sugar to `add_command` method.
        Using this decorator, it is possible to register commands as follows

        >>> dispatcher = CommandDispatcher()
        >>> @dispatcher.command(r'^/hello (?P<name>\w+)$')
        ... def greet(name):
        ...     print('Hello, {}!'.format(name))
        ...
        >>> dispatcher.run_command('/hello world')
        Hello, world!

        Arguments:
        pattern -- Python regex pattern. See `add_command` method.
        """
        def decorator(callback):
            self.add_command(pattern, callback)
            return callback

        return decorator

    def run_command(self, command):
        """Run the given command.

        This method will invoke the registered callback function whose pattern
        matches the the given command text. See example on `add_command` method.
        """
        for prog, callback in self._command_list:
            match = prog.search(command)
            if match is not None:
                return callback(*match.groups())
        raise CommandNotFoundError('No matching command for {}'.format(command))
