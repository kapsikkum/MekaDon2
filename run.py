# -*- coding: utf-8 -*-
# @Author: kapsikkum
# @Date:   2021-02-25 01:28:13
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-02-27 17:42:26


import yaml
import os
from core import bot
from core.events import init_events

config = yaml.load(open("config.yml").read(), Loader=yaml.FullLoader)

bot.run(config["token"])
