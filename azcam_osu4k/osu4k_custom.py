"""
Contains the OSU4k class.
"""

import azcam


class OSU4k(object):
    """
    Class definition of OSU4k customized commands.
    These methods are called remotely through the command server with syntax such as:
    osu4k.test 1.0 "some_text".
    """

    def __init__(self):
        """
        Creates osu4k tool.
        """

        azcam.db.tools["osu4k"] = self

        return

    def initialize(self):
        """
        Initialize OSU4k stuff.
        """

        return

    def test(self, foo: float = 1.0, bar: str = "") -> str:
        """
        A dummy method.
        """

        return "OK"
