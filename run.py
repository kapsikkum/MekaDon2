# -*- coding: utf-8 -*-
# @Author: kapsikkum
# @Date:   2021-02-25 01:28:13
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-02 14:08:44


import logging
import os
import sys

import yaml

from mecha.core import bot
from mecha.core.events import init_events

logger = logging.getLogger("mecha")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("(%(asctime)s) <[%(levelname)s] %(name)s>: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

config = yaml.load(open("config.yml").read(), Loader=yaml.FullLoader)

bot.run(config["token"])
