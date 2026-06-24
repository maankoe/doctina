
def scramble(original, n: int=128, rounds: list[int]=None):
    half_n = n // 2
    left = original >> half_n 
    right = original & ((1 << half_n) - 1)
    for round in rounds or []:
        seed = feistel_round(right, round, half_n) 
        new_right = left ^ seed
        left = right
        right = new_right
    return (left << half_n) + right

def unscramble(scrambled, n: int=128, rounds: list[int]=None, original=None):
    half_n = n // 2
    left = scrambled >> half_n
    right = scrambled & ((1 << half_n) - 1)
    for round in reversed(rounds or []):
        seed = feistel_round(left, round, half_n)
        old_left = right ^ seed
        right = left
        left = old_left
    return (left << half_n) + right

def feistel_round(block, round_constant, half_n):
    def split_shift(n_ratio: int):
        a = half_n // n_ratio 
        b = half_n - a
        return ((mixed << a) | (mixed >> b)) & ((1 << half_n) - 1)
    mixed = round_constant ^ block & ((1 << half_n) - 1) 
    mixed = split_shift(6)
    mixed = (mixed * 0x6c8e944d1f5aa3b7) & ((1 << half_n) - 1)
    return split_shift(3)

def encode_index(value: int, padding: int=32) -> str:
    return f"{value:0>{padding}X}"

def encode_binary(value: int, n=32) -> str:
    return f"{value:0{n}b}"

if __name__ == "__main__":
    n = 128 
    rounds = [n//5, n//15, n]
    for a in range(1, 2**n):
        scrambled = scramble(a, n, rounds)
        unscrambled = unscramble(scrambled, n, rounds, original=a)
        #print(a,
        #      encode_binary(a, n),
        #      ",".join([encode_binary(x, n) for x in rounds]),
        #      encode_binary(scrambled, n),
        #      encode_binary(unscrambled, n),
        #      )
        print(a,
              encode_index(a, n//4),
              ",".join([encode_index(x, n//4) for x in rounds]),
              encode_index(scrambled, n//4),
              encode_index(unscrambled, n//4),
              )
