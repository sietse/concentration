#!/usr/bin/env python
"""Concentration

A very simple command line application to maintain focus by blocking distracting sites.
"""
import codecs
import subprocess
import sys
import time

from pathlib import Path

import hug

from blessings import Terminal

from . import settings


if sys.version_info[0] < 3:
    input = raw_input
else:
    input = input


def reset_network(message):
    """Resets the users network to make changes take effect"""
    for command in settings.RESTART_NETWORK:
        try:
            subprocess.check_call(command)
        except:
            pass
    print(message)


def does_the_user_really_want_this(time_to_think=60):
    """
    Give the user time to change their mind. Return False if
    they hit Ctrl-C in that time, otherwise True
    """
    print("")
    print("######################################### ARE YOU SURE? #####################################")

    # Print the things that are left to do
    todofile = Path.home() / 'todo.txt'
    print("")
    if todofile.exists():
        term = Terminal()
        with open(str(todofile), "r") as f:
            for line_with_newline in f.readlines():
                line = line_with_newline[:-1]
                if line.startswith('(A)'):
                    print(term.cyan(line))
                elif line.startswith('(B)'):
                    print(term.bright_yellow(line))
                elif line.startswith('(C)'):
                    print(term.bright_green(line))
                elif line.startswith('x '):
                    print(term.bold_bright_cyan(line))
                else:
                    print(line)
    print("")

    try:
        for remaining in range(time_to_think, -1, -1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} seconds to change your mind. Won't you prefer programming? Or a book?".format(remaining))
            sys.stdout.flush()
            time.sleep(1)
        return True
    except KeyboardInterrupt:
        print("")
        print("")
        print(":D :D :D\nGood on you! <3")
        return False


@hug.cli()
def improve():
    """Disables access to websites that are defined as 'distractors'"""
    with open(settings.HOSTS_FILE, "r+") as hosts_file:
        contents = hosts_file.read()
        if not settings.START_TOKEN in contents and not settings.END_TOKEN in contents:
            hosts_file.write(settings.START_TOKEN + "\n")
            for site in set(settings.DISTRACTORS):
                hosts_file.write("{0}\t{1}\n".format(settings.REDIRECT_TO, site))
                for sub_domain in settings.SUB_DOMAINS:
                    hosts_file.write("{0}\t{1}.{2}\n".format(settings.REDIRECT_TO, sub_domain, site))
            hosts_file.write(settings.END_TOKEN + "\n")

    reset_network("Concentration is now improved :D!")


@hug.cli()
def lose():
    """Enables access to websites that are defined as 'distractors'"""
    if not does_the_user_really_want_this(time_to_think=60):
        return

    changed = False
    with open(settings.HOSTS_FILE, "r") as hosts_file:
        new_file = []
        in_block = False
        for line in hosts_file:
            if in_block:
                if line.strip() == settings.END_TOKEN:
                    in_block = False
                    changed = True
            elif line.strip() == settings.START_TOKEN:
                in_block = True
            else:
                new_file.append(line)
    if changed:
        with open(settings.HOSTS_FILE, "w") as hosts_file:
            hosts_file.write("".join(new_file))

    reset_network("Concentration is now lost :(.")


seconds = int

def duration(text: str) -> seconds:
    """For example `1`, `1m`, or `60s`"""
    if text == '':
        text = input('Break for how long (1m, 30s, ...)? ')

    head, tail = text[:-1], text[-1]

    if tail == 'm':
        return int(head) * 60
    elif tail == 's':
        return int(head)
    elif tail in '1234567890':
        return int(text) * 60
    else:
        raise ValueError("Duration should look like '1', '1m', or '60s'")


@hug.cli('break')
def take_break(duration: duration=''):
    """Enables temporarily breaking concentration"""

    if not does_the_user_really_want_this(time_to_think=60):
        return

    # The user insisted on breaking concentration.
    lose()
    print("")
    print("######################################### TAKING A BREAK ####################################")
    try:
        for remaining in range(duration, -1, -1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} seconds remaining without concentration.".format(remaining))
            sys.stdout.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\rEnough distraction!                                                            \n")
        print("######################################### BREAK OVER :) #####################################")
        print("")
        improve()


@hug.cli()
def blocked():
    """Returns the configured list of blocked sites"""
    return settings.DISTRACTORS


@hug.cli('64')
def game():
    """Basic game implementation"""
    print(codecs.encode('Sbe Nznaqn, gur ybir bs zl yvsr', 'rot_13'))
