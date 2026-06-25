from math import ceil
from random import shuffle
from cipher import scramble, unscramble

NUM_BITS = 128
cipher_rounds = [NUM_BITS//5, NUM_BITS//15, NUM_BITS]


class Dataset:
    def __init__(self, num_bits: int=NUM_BITS):
        self._num_bits = num_bits
        self._padding = ceil(self._num_bits/4)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return (self[x] for x in range(key.start or 0, key.stop or self.size(), key.step or 1))
        return encode_index(scramble(key, self._num_bits, cipher_rounds), self._padding)

    def __iter__(self):
        for x in range(0, self.size()):
            yield self[x]

    def size(self):
        return 2**self._num_bits

    def slow_search(self, s: str, start: int=0):
        s = s.upper()
        for i, x in enumerate(self[start:], start):
            if s in x:
                return i

    def search(self, s: str, start: int=0):
        s = s.upper()
        int_s = decode_index(s)
        n_bits = binary_len(int_s) 
        fill_bits = self._num_bits - n_bits
        fill_data = Dataset(num_bits=fill_bits)
        for i, x in enumerate(fill_data):
            for j, p in enumerate(range(len(x))):
                found = f"{x[:p]}{s}{x[p:]}"
                findex = decode_index(found)
                unscrambled = unscramble(findex, n=self._num_bits, rounds=cipher_rounds)
                #print(i, j, found, findex, unscrambled) 
                yield unscrambled


def binary_len(value: int) -> str:
    return len(f"{value:b}")

def decode_index(s: str) -> int:
    return int(s, 16)

def encode_index(value: int, padding: int=32) -> str:
    return f'{value:0>{padding}X}'


if __name__ == "__main__":
    import time
    data = Dataset()

    for s in ["a", "aa", "aaa", "aaaa", "aaaaa", "aaaaaa", "aaaaaaa"]:
        start = time.time()
        i = data.search(s)
        print(s, i, data[i], f"{(time.time() - start):.2f}")



