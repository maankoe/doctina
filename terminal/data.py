from typing import Callable
from math import ceil
from random import shuffle
from cipher import scramble, unscramble


NUM_BITS = 128
cipher_rounds = [NUM_BITS//5, NUM_BITS//15, NUM_BITS]


class Dataset:
    def __init__(self, num_bits: int=NUM_BITS, encode_index: Callable[[int], str]=None):
        self._num_bits = num_bits
        self._encode_index = encode_index or create_uuid4_index_encoder()

    def __getitem__(self, key):
        if isinstance(key, slice):
            return (self[x] for x in range(key.start or 0, key.stop or self.size(), key.step or 1))
        return self._encode_index(scramble(key, self._num_bits, cipher_rounds))

    def __iter__(self):
        for x in range(0, self.size()):
            yield self[x]

    def size(self):
        return 2**self._num_bits

    def search(self, s: str, start: int=0):
        s = s.upper()
        int_s = decode_index(s)
        n_bits = binary_len(int_s) 
        fill_bits = self._num_bits - n_bits
        fill_data = Dataset(
                num_bits=fill_bits, 
                encode_index=create_index_encoder(fill_bits),
        )
        for i, x in enumerate(fill_data):
            for j, p in enumerate(range(len(x))):
                found = f"{x[:p]}{s}{x[p:]}"
                findex = decode_index(found)
                unscrambled = unscramble(findex, n=self._num_bits, rounds=cipher_rounds)
                yield unscrambled
    

def binary_len(value: int) -> str:
    return len(f"{value:b}")


def create_index_encoder(num_bits: int) -> Callable[[int], str]:
    padding = ceil(num_bits/4)
    return lambda value: f"{value:0>{padding}X}"

def create_uuid4_index_encoder() -> Callable[[int], str]:
    # xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
    # AF6C00C6-0816-FA64-B229-E5A7BA89A5CC
    def _encode(value: int) -> str:
        s = f"{value:0>32X}"
        return f"{s[:8]}-{s[8:12]}-{s[12:16]}-{s[16:20]}-{s[20:]}"
    return _encode

def decode_index(s: str) -> int:
    return int(s, 16)


if __name__ == "__main__":
    import time
    data = Dataset()

    for s in ["a", "aa", "aaa", "aaaa", "aaaaa", "aaaaaa", "aaaaaaa"]:
        start = time.time()
        i = data.search(s)
        print(s, i, data[i], f"{(time.time() - start):.2f}")



