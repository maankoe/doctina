from dataclasses import dataclass
from collections.abc import Iterable
from data import Dataset
from search import Search, Direction


class Context:
    def __init__(self, data: Dataset, start_index: int = 0):
        self._data = data
        self._index = start_index
        self._search = None
        self._height = 250
        self._max_index = data.size()

    @property
    def index(self) -> int:
        return self._index

    def down(self, n: int = 1):
        self.goto(self._index + n)

    def up(self, n: int = 1):
        self.goto(self._index - n)

    def set_search(self, s: str | None = None, direction: Direction = Direction.DOWN):
        if s is None and not self._search:
            raise ValueError("Cannot pass empty search without existing search")
        if self._search and not s:
            if self._search.direction is not direction:
                self._search.reverse()
            return
        if s or self._search != s:
            self._search = Search(self._data, s, direction)

    def clear_search(self):
        self._search = None

    def next(self):
        if self._search is not None:
            self.goto(self._search.next())
        else:
            self.down()

    def goto(self, index: int):
        if index < 0:
            index = 0
        elif index > self._max_index - self._height:
            index = self._max_index - self._height + 1
        self._index = index
