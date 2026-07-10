from data import Dataset, binary_len, decode_index, create_index_encoder, unscramble
from data import _is_valid_uuid4, cipher_rounds


class Search:
    def __init__(self, data: Dataset, s: str, reversed: bool=False):
        self._data = data
        self._s = s.upper()
        self._reversed = reversed

        self._s_chars = self._s.replace("-", "")
        fill_bits = self._data.num_bits() - binary_len(decode_index(self._s_chars))
        self._fill_data = Dataset(
                num_bits=fill_bits,
                encode_index=create_index_encoder(fill_bits),
        )
        self._fill_data_index = 0
        self._insert_pos = 0
        if self._reversed:
            self._next_index()

    def reverse(self):
        self._reversed = not self._reversed
        self._next_index()
        self._next_index()

    def next(self):
        while True:
            x = self._fill_data[self._fill_data_index]
            found = f"{x[:self._insert_pos]}{self._s_chars}{x[self._insert_pos:]}"
            findex = decode_index(found)
            self._next_index()
            if not _is_valid_uuid4(findex):
                continue
            unscrambled = unscramble(findex, n=self._data.num_bits(), rounds=cipher_rounds)
            if self._s not in self._data[unscrambled]:
                print("NOT", self._data[unscrambled])
                continue
            return unscrambled


    def _next_index(self):
        #print(self._insert_pos, self._fill_data_index, self._fill_data.num_bits()/4, self._reversed)
        if self._reversed:
            if self._insert_pos == 0:
                self._insert_pos = self._fill_data.num_bits()//4 
                if self._fill_data_index == 0:
                    self._fill_data_index = self._fill_data.size() - 1 
                else:
                    self._fill_data_index -= 1
            else:
                self._insert_pos -= 1
        else:
            if self._insert_pos >= self._fill_data.num_bits()/4:
                self._insert_pos = 0
                if self._fill_data_index >= self._fill_data.size():
                    self._fill_data_index = 0
                else:
                    self._fill_data_index += 1
            else:
                self._insert_pos += 1
        #print(self._insert_pos, self._fill_data_index, self._fill_data.num_bits()/4)


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


