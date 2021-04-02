# -*- coding: utf-8 -*-
# @Author: kapsikkum
# @Date:   2021-02-28 16:19:51
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-02 06:51:27

import sqlalchemy as db

metadata = db.MetaData()


from .user import User
from .tag import Tag