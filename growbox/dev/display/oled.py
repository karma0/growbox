# -*- coding: utf-8 -*-

"""Display module"""

import os
import sys
import time
import logging

from luma.core.render import canvas
from PIL import ImageFont

from growbox.dev.display.demo_opts import get_device


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Display:
    device = get_device()

    display_texts = []

    def __init__(self):
        font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                    'fonts', 'C&C Red Alert [INET].ttf'))
        logger.info(f"Using font path: {font_path}")
        self.font2 = ImageFont.truetype(font_path, 12)

    def show(self):
        with canvas(self.device) as draw:
            offset = 0
            for row in self.display_texts:
                draw.text((0, offset), row, font=self.font2, fill='white')
                offset += 14

    def __call__(self, data):
        logger.info(f"Displaying data: {data}")
        self.display_texts = [f"{key}: val" for key, val in data]
        self.show()
