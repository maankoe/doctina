import shutil
import sys,tty,os,termios




def getkey():
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    try:
        while True:
            b = os.read(sys.stdin.fileno(), 3).decode()
            if len(b) == 3:
                k = ord(b[2])
            else:
                k = ord(b)
            key_mapping = {
                127: "backspace",
                10: "return",
                32: "space",
                9: "tab",
                113: "q",
                27: "esc",
                65: "up",
                66: "down",
                67: "right",
                68: "left",
                47: "/",
                58: ":",
                63: "?",
            }
            return key_mapping.get(k, chr(k))
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def main():
    data = Dataset()
    pager = Pager(data, 0)
    pager.draw()
    try:
        while True:
            k = getkey()
            if k in ["esc", "q"]:
                quit()
            elif k in ["down", "return"]:
                pager.index += 1
                pager.draw()
            elif k == "up":
                pager.index -= 1
                pager.draw()
            elif k == ":":
                pager.index = int(input(":"))
                pager.draw()
            elif k == "/":
                s = input("/")
                pager.index = data.search(s, pager.index)
                pager.draw()
            else:
                try:
                    print(k, ord(k))
                except:
                    print(k, "?")
    except (KeyboardInterrupt, SystemExit):
        os.system("stty sane")
        print("stopping.") 


class Dataset:
    def __init__(self, num_bits: int=16):
        self._num_bits = num_bits

    def __getitem__(self, key):
        if isinstance(key, slice):
            return (encode_index(x) for x in range(key.start or 0, key.stop or len(self), key.step or 1))
        return encode_index(key)

    def __len__(self):
        return 2**self._num_bits

    def search(self, s, start):
        s = s.upper()
        for i, x in enumerate(self[start:], start):
            if s in x:
                return i

class Pager:
    def __init__(self, data, index=0):
        self._data = data
        self._index = index
        _, height = shutil.get_terminal_size((80, 20))
        self._height = height

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        if index < 0:
            index = 0
        elif index > len(self._data) - self._height:
            index = len(self._data) - self._height + 1
        self._index = index

    def draw(self):
        paint(self._data[self._index:self._index+self._height-1])


def encode_index(value: int, padding: int=32) -> str:
    return f'{value:0>{padding}X}'


def paint(lines):
    print("\033[2J\033[H" + "\n".join(lines))


if __name__ == "__main__":
    main()
