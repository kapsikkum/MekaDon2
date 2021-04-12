# @Author: kapsikkum
# @Date:   2021-04-12 13:05:07
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-12 13:44:26


class ExpireList(list):
    def __init__(self, initlist=None, max_length=100) -> None:
        self.max_length = max_length
        super().__init__(initlist if initlist is not None else list())

    def append(self, item):
        list.append(self, item)
        if len(self) > self.max_length:
            del self[0]

    def remove(self, item):
        list.remove(self, item)

    def __lt__(self, other):
        return len(self) < other

    def __le__(self, other):
        return len(self) <= other

    def __gt__(self, other):
        return len(self) > other

    def __ge__(self, other):
        return len(self) >= other

    def __eq__(self, other):
        return len(self) == other

    def __ne__(self, other):
        return not (self.__eq__(self, other))
