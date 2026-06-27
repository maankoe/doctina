

class Context:
    def __init__(self, max_index: int, start_index: int=0):
        self._index = start_index
        self._search = None
        self._height = 250
        self._max_index = max_index

    @property
    def index(self) -> int:
        return self._index

    def down(self, n: int=1):
        self.goto(self._index + n)

    def up(self, n: int=1):
        self.goto(self._index - n)

    def set_search(self, search):
        self._search = search
        self.next()

    def next(self):
        if self._search is not None:
            self.goto(next(self._search))
        else:
            self.down()

    #def previous(self):
    #    if self._search is not None:
    #        self._set_index(self.search.previous)
    #    else:
    #        self.up()

    def goto(self, index: int):
        if index < 0:
            index = 0
        elif index > self._max_index - self._height:
            index = self._max_index - self._height + 1
        self._index = index
        
