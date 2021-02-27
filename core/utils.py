# -*- coding: utf-8 -*-
# @Author: kapsikkum
# @Date:   2021-02-25 03:01:41
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-02-25 03:02:15


import subprocess


def get_version():
    return (
        subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        .strip()
        .decode()
    )
