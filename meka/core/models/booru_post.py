# @Author: kapsikkum
# @Date:   2021-04-03 03:07:25
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-03 03:09:59


class BooruPost:
    """
    The object from booru clients
    """

    def __init__(self, file_url, post_url) -> None:
        self.file_url = file_url
        self.post_url = post_url