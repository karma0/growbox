# -*- coding: utf-8 -*-

"""Display module"""

import os
import sys
import time

from demo_opts import get_device
from luma.core.render import canvas
from PIL import ImageFont


class Display:
    device = get_device()

    display_texts = []

    def __init__(self):
        font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                    'fonts', 'C&C Red Alert [INET].ttf'))
        self.font2 = ImageFont.truetype(font_path, 12)

    def show(self):
        with canvas(self.device) as draw:
            offset = 0
            for row in self.display_texts:
                draw.text((0, offset), row, font=self.font2, fill='white')
                offset += 14
