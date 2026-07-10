from typing import Callable
from math import ceil
from random import shuffle
from cipher import scramble

NUM_BITS = 122
cipher_rounds = [NUM_BITS // 5, NUM_BITS // 15, NUM_BITS]


class Dataset:
    def __init__(
        self,
        num_bits: int = NUM_BITS,
        encode_index: Callable[[int], str] = None,
        reversed: bool = False,
    ):
        self._num_bits = num_bits
        self._encode_index = encode_index or create_uuid4_index_encoder()
        self._reversed = reversed

    def __getitem__(self, key):
        if isinstance(key, slice):
            return (
                self[x]
                for x in range(key.start or 0, key.stop or self.size(), key.step or 1)
            )
        return self._encode_index(scramble(key, self._num_bits, cipher_rounds))

    def __iter__(self):
        for x in rrange(0, self.size(), self._reversed):
            yield self[x]

    def num_bits(self) -> int:
        return self._num_bits

    def size(self) -> int:
        return 2**self._num_bits


def rrange(start: int, stop: int, reversed: bool = False):
    if reversed:
        return range(stop - 1, start - 1, -1)
    return range(start, stop)


def create_uuid4_index_encoder() -> Callable[[int], str]:
    # xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
    # AF6C00C6-0816-FA64-B229-E5A7BA89A5CC
    # XXXXXXXX-XXXX     - take these 48 bits from left
    # 4XXX              - skip the next 4 bits (for the version)
    #                     and take 12 more bits from left
    # V                 - skip the next 2 bits (for the variant)
    #                     and add the last bit from left
    # XXX-XXXXXXXXXXXX  - the lower 61 bits come from right
    def _encode(value: int) -> str:
        value &= (1 << 122) - 1
        lower_62 = value & ((1 << 62) - 1)
        mid_12 = (value >> 62) & ((1 << 12) - 1)
        upper_48 = (value >> 74) & ((1 << 48) - 1)

        result = 0
        result |= upper_48 << 80  # Shift upper bits to the top
        result |= 4 << 76  # Inject version 4 (bits 76-79)
        result |= mid_12 << 64  # Inject middle bits (bits 64-75)
        result |= 2 << 62  # Inject variant '10' (bits 62-63)
        result |= lower_62  # Inject remaining lower bits (bits 0-61)
        s = f"{result:0>32X}"
        return f"{s[:8]}-{s[8:12]}-{s[12:16]}-{s[16:20]}-{s[20:]}"

    return _encode


if __name__ == "__main__":
    import time

    data = Dataset()

    for s in ["a", "aa", "aaa", "aaaa", "aaaaa", "aaaaaa", "aaaaaaa"]:
        start = time.time()
        i = data.search(s)
        print(s, i, data[i], f"{(time.time() - start):.2f}")
