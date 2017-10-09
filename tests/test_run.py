"""test_concentration.py

Basic testing to ensure concentration will load

Copyright (C) 2013  Timothy Edmund Crosley

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

"""
from concentration import run, settings


def test_settings():
    assert settings.PLATFORM in (settings.OS.linux, settings.OS.mac, settings.OS.windows)
    assert settings.HOSTS_FILE and isinstance(settings.HOSTS_FILE, str)
    assert settings.DISTRACTORS and isinstance(settings.DISTRACTORS, (set))


def test_parse_duration():
    assert run.parse_duration('2m') == 120  # parse minutes
    assert run.parse_duration('30s') == 30  # parse seconds
    assert run.parse_duration('1') == 60  # default to minutes
    assert run.parse_duration('2') == 120
