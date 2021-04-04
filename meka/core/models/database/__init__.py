# -*- coding: utf-8 -*-
# @Author: kapsikkum
# @Date:   2021-02-28 16:19:51
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-04 03:36:09

import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient()

from .user import User
from .tag import Tag