# -*- coding: utf-8 -*-

"""Console script for growbox."""
import sys
import click

import logging

from growbox.growbox import GrowBox


logger = logging.getLogger(__name__)


@click.command()
def main(args=None):
    """Console script for growbox."""
    while True:
        try:
            box = GrowBox()
            box.run()
        except Exception as ex:
            logger.error(str(ex))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
