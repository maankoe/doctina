from dataclasses import dataclass
from collections.abc import Iterable
from data import Dataset

@dataclass(frozen=True)
class Search:
    s: str
    iterator: Iterable[int] 
    reversed: bool


class Context:
    def __init__(self, data: Dataset, start_index: int=0):
        self._data = data
        self._index = start_index
        self._search = None
        self._height = 250
        self._max_index = data.size()

    @property
    def index(self) -> int:
        return self._index

    def down(self, n: int=1):
        self.goto(self._index + n)

    def up(self, n: int=1):
        self.goto(self._index - n)

    def set_search(self, s: str | None=None, reversed: bool=False):
        if s is None and not self._search:
            raise ValueError("Cannot pass empty search without existing search")
        if self._search and self._search.s == s and self._search.reversed == reversed:
            self.next()
            return
        resolved_s = s or self._search.s
        self._search = Search(resolved_s, self._data.search(resolved_s, self._index, reversed=reversed), reversed)
        self.next()

    def clear_search(self):
        self._search = None

    def next(self):
        if self._search is not None:
            self.goto(next(self._search.iterator))
        else:
            self.down()

    def goto(self, index: int):
        if index < 0:
            index = 0
        elif index > self._max_index - self._height:
            index = self._max_index - self._height + 1
        self._index = index
        
