ROUND_CONSTANTS = [
        0x47f5417d6b82b5d1,
        0x90a7c5fe8c345af2,
        0xd8796c3b2a1e4f8d,
        0x6f4a3c8e7d5b9102,
        0xb3f8c7d6e5a49201,
        0x2d9e8b7c6f5a3d4e,
        0xa1b2c3d4e5f6789a,
        0x123456789abcdef0,
];

def scramble(unscrambled):
    left = i >> 64
    right = i & 2**64-1
    for round in ROUND_CONSTANTS:
        seed = feistel_round(right, round) # seed is a function of right
        newRight = left ^ seed # new right is XOR of old left and the seed
        left = right # new left side is the old right side
        right = newRight
    return (left << 64) + right

def unscramble(scrambled):
    left = i >> 64
    right = i & 2**64-1
    for round in reversed(ROUND_CONSTANTS):
        oldRight = left
        seed = feistel_round(oldRight, round)
        oldLeft = right ^ seed
        left = oldLeft
        right = oldRight
    return (left << 64) + right


def feistel_round(block, round_constant):
    return block ^ round_constant
    # Mix using rotations, XORs, and addition, maintaining 61-bit blocks
    mixed = block
    mixed ^= round_constant & ((1 << 61) - 1)
    mixed = ((mixed << 7) | (mixed >> 54)) & ((1 << 61) - 1)
    mixed = (mixed * 0x6c8e944d1f5aa3b7) & ((1 << 61) - 1)
    mixed = ((mixed << 13) | (mixed >> 48)) & ((1 << 61) - 1)
    return mixed;


def encode_index(value: int, padding: int=32) -> str:
    return f'{value:0>{padding}X}'


if __name__ == "__main__":
    for i in range(2**32-20, 2**32+20):
        print(encode_index(i), encode_index(scramble(i)), encode_index(unscramble(scramble(i))))
        #print(i, hex(i), bin(i), bin(i >> 32), bin(i & 2**32-1))

