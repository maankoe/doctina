import shutil
from data import Dataset
from keymap import get_key
from context import Context


def main():
    data = Dataset()
    context = Context(data.size())
    pager = Pager(data, context)
    pager.draw()
    try:
        while True:
            k = get_key()
            if k in ["esc", "q"]:
                quit()
            elif k in ["down"]:
                context.down()
            elif k == "up":
                context.up()
            elif k == ":":
                x = int(input(":"))
                context.goto(x)
            elif k in ["return"]:
                context.next()
            elif k == "/":
                s = input("/")
                if s:
                    context.set_search(data.search(s, context.index))
                else:
                    context.next()
            else:
                try:
                    print(k, ord(k))
                except:
                    print(k, "?")
            pager.draw()
    except (KeyboardInterrupt, SystemExit):
        os.system("stty sane")
        print("stopping.") 


class Pager:
    def __init__(self, data, context):
        self._data = data
        self._context = context
        _, height = shutil.get_terminal_size((80, 20))
        self._height = height

    def draw(self):
        start = self._context.index
        lines = self._data[start:start+self._height-1] 
        print("\033[2J\033[H" + "\n".join(lines))


if __name__ == "__main__":
    main()
