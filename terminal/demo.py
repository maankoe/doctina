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
            if k == "esc":
                quit()
            elif k == "down":
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
                print(k, ord(k))
    except (KeyboardInterrupt, SystemExit):
        os.system("stty sane")
        print("stopping.")       

class Dataset:
    def __init__(self):
        self._data = [str(x) for x in range(100)]

    def __getitem__(self, key):
        return self._data[key]

    def __len__(self):
        return len(self._data)

    def search(self, s, start):
        for i, x in enumerate(self._data[start:]):
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

        
def paint(lines):
    print("\033[2J\033[H" + "\n".join(lines))


if __name__ == "__main__":
    main()
