# @Author: kapsikkum
# @Date:   2021-04-20 09:01:03
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-20 09:28:00


class CommandErrorNotification(Exception):
    """Used for expected errors."""


class YTDLError(Exception):
    """Used for YTDL errors"""