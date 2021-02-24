# -*- coding: utf-8 -*-
# @Author: kapsikkum
# @Date:   2021-02-25 01:28:13
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-02-25 02:53:29
import yaml
import os
from core import bot

print(os.listdir())
config = yaml.load(open("./mecha/config.yml").read(), Loader=yaml.FullLoader)
print(config)
bot.run(config["token"])
