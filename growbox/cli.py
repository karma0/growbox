# -*- coding: utf-8 -*-

"""Console script for growbox."""
import sys
import click

from growbox.growbox import GrowBox


@click.command()
def main(args=None):
    """Console script for growbox."""
    box = GrowBox()
    box.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
