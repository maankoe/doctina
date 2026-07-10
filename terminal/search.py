from data import Dataset
from cipher import unscramble
from data import cipher_rounds
from enum import Enum
from math import ceil


class Direction(Enum):
    UP = 0
    DOWN = 1


class Search:
    def __init__(self, data: Dataset, s: str, direction: Direction = Direction.DOWN):
        self._data = data
        self._s = s.upper()
        self._direction = direction

        self._s_chars = self._s.replace("-", "")
        fill_bits = self._data.num_bits() - binary_len(decode_index(self._s_chars))
        self._fill_data = Dataset(
            num_bits=fill_bits,
            encode_index=create_index_encoder(fill_bits),
        )
        self._fill_data_index = 0
        self._insert_pos = 0
        if self._direction is Direction.UP:
            self._next_index()  # go to end

    @property
    def search_str(self) -> str:
        return self._s

    @property
    def direction(self) -> Direction:
        return self._direction

    def set_direction(self, direction: Direction):
        self._direction = direction
        self._next_index()
        self._next_index()

    def reverse(self):
        if self._direction is Direction.DOWN:
            self.set_direction(Direction.UP)
        else:
            self.set_direction(Direction.DOWN)

    def next(self):
        while True:
            x = self._fill_data[self._fill_data_index]
            found = f"{x[:self._insert_pos]}{self._s_chars}{x[self._insert_pos:]}"
            findex = decode_index(found)
            self._next_index()
            if not _is_valid_uuid4(findex):
                continue
            unscrambled = unscramble(
                findex, n=self._data.num_bits(), rounds=cipher_rounds
            )
            if self._s not in self._data[unscrambled]:
                print("NOT", self._data[unscrambled])
                continue
            return unscrambled

    def _next_index(self):
        if self._direction is Direction.UP:
            if self._insert_pos == 0:
                self._insert_pos = self._fill_data.num_bits() // 4
                if self._fill_data_index == 0:
                    self._fill_data_index = self._fill_data.size() - 1
                else:
                    self._fill_data_index -= 1
            else:
                self._insert_pos -= 1
        else:
            if self._insert_pos >= self._fill_data.num_bits() / 4:
                self._insert_pos = 0
                if self._fill_data_index >= self._fill_data.size():
                    self._fill_data_index = 0
                else:
                    self._fill_data_index += 1
            else:
                self._insert_pos += 1


def create_index_encoder(num_bits: int) -> Callable[[int], str]:
    padding = ceil(num_bits / 4)
    return lambda value: f"{value:0>{padding}X}"


def decode_index(s: str) -> int:
    return int(s, 16)


def binary_len(value: int) -> str:
    return len(f"{value:b}")


def _is_valid_uuid4(value: int) -> bool:
    if not (0 <= value <= 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF):
        return False
    version = (value >> 76) & 0xF
    if version != 4:
        return False
    variant = (value >> 62) & 0x3
    if variant != 2:
        return False
    return True


if __name__ == "__main__":
    import time

    data = Dataset(num_bits=16, encode_index=create_index_encoder(16))

    search = Search(data, "aaa")
    for i, x in enumerate(range(37)):
        fi = search.next()
        print(data[fi], i, fi, data[fi])
    search.reverse()
    print("------")
    for i, x in enumerate(range(37)):
        fi = search.next()
        print(data[fi], i, fi, data[fi])
