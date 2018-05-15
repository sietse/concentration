import configparser
import functools
import subprocess
import sys


def get_hooks(prefix, config):
    """Return matching hooks from the config.

    'Matching' means 'entries whose names starts with `prefix` in the
    'hooks' section of the `config` object.' Matches are returned in
    alphabetical order.

    Returns
    -------
    (name, value)
        hooks' name and contents
    """
    if 'hooks' not in config:
        return []

    return sorted([
        (name, value)
        for name, value in config['hooks'].items()
        if name.startswith(prefix)
    ])


def plus_hooks(function):
    """Wrap function so that pre- and post-hooks are run around the call.

    The pre-hooks are shell scripts, taken from the 'hooks' section of
    the config object. They are run in alphabetical order. As soon as
    one hook has a non-zero exit code, subsequent hooks and the function
    itself are not run.

    The post-hooks, too, are shell scripts. They, too, are run in order;
    hook failure is ignored

    >>> myconfig = {'hooks': {'pre-test': 'false'}}
    >>> @plus_hooks
    ... def test():
    ...     return 8
    ...
    >>> try:
    ...     test(config=myconfig)
    ... except SystemExit:
    ...     pass
    Abort: pre-test returned exit code 1
    """
    try:
        global CONFIG
        config = CONFIG
    except NameError:
        config = configparser.ConfigParser().read_dict({})

    func_name = function.__name__
    @functools.wraps(function)
    def wrapped_function(*args, config=config, **kwargs):
        # run pre-hooks, exit if one fails
        for hook_name, hook in get_hooks(f'pre-{func_name}', config):
            exit_code = subprocess.call(hook, shell=True)
            if exit_code:
                print(f'Abort: {hook_name} returned exit code {exit_code}')
                sys.exit(exit_code)
        # run function
        function(*args, **kwargs)
        # run post-hooks, ignore failure
        for hook_name, hook in get_hooks(f'post-{func_name}', config):
            subprocess.call(hook, shell=True)
    return wrapped_function


if __name__ == '__main__':
    import doctest
    doctest.testmod()
