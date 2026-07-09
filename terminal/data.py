from typing import Callable
from math import ceil
from random import shuffle
from cipher import scramble, unscramble


NUM_BITS = 122
cipher_rounds = [NUM_BITS//5, NUM_BITS//15, NUM_BITS]


class Dataset:
    def __init__(self, num_bits: int=NUM_BITS, encode_index: Callable[[int], str]=None,
                 reversed: bool=False):
        self._num_bits = num_bits
        self._encode_index = encode_index or create_uuid4_index_encoder()
        self._reversed = reversed

    def __getitem__(self, key):
        if isinstance(key, slice):
            return (self[x] for x in range(key.start or 0, key.stop or self.size(), key.step or 1))
        return self._encode_index(scramble(key, self._num_bits, cipher_rounds))

    def __iter__(self):
        for x in rrange(0, self.size(), self._reversed):
            yield self[x]

    def num_bits(self) -> int:
        return self._num_bits

    def size(self) -> int:
        return 2**self._num_bits

    def search(self, s: str, start: int=0, reversed=False):
        s = s.upper()
        s_chars = s.replace("-", "")
        n_bits = binary_len(decode_index(s_chars)) 
        fill_bits = self._num_bits - n_bits
        fill_data = Dataset(
                num_bits=fill_bits, 
                encode_index=create_index_encoder(fill_bits),
                reversed=reversed,
        )
        for i, x in enumerate(fill_data):
            for j, p in enumerate(rrange(0, len(x))):
                found = f"{x[:p]}{s_chars}{x[p:]}"
                findex = decode_index(found)
                if not _is_valid_uuid4(findex):
                    continue
                if s not in self._encode_index(findex):
                    continue
                yield unscramble(findex, n=self._num_bits, rounds=cipher_rounds)
    

def rrange(start: int, stop: int, reversed: bool=False):
    if reversed:
        return range(stop-1, start-1, -1)
    return range(start, stop)


def binary_len(value: int) -> str:
    return len(f"{value:b}")


def create_index_encoder(num_bits: int) -> Callable[[int], str]:
    padding = ceil(num_bits/4)
    return lambda value: f"{value:0>{padding}X}"


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
        result |= 4 << 76         # Inject version 4 (bits 76-79)
        result |= mid_12 << 64     # Inject middle bits (bits 64-75)
        result |= 2 << 62         # Inject variant '10' (bits 62-63)
        result |= lower_62        # Inject remaining lower bits (bits 0-61)
        s = f"{result:0>32X}"
        return f"{s[:8]}-{s[8:12]}-{s[12:16]}-{s[16:20]}-{s[20:]}"
    return _encode


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


def decode_index(s: str) -> int:
    return int(s, 16)


if __name__ == "__main__":
    import time
    data = Dataset()

    for s in ["a", "aa", "aaa", "aaaa", "aaaaa", "aaaaaa", "aaaaaaa"]:
        start = time.time()
        i = data.search(s)
        print(s, i, data[i], f"{(time.time() - start):.2f}")



