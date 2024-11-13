import curses
import sys
import util
from string import ascii_lowercase

ROW, COL = 0, 1
test_screen_size = None#(20, 20)

def main(stdscr, lines):
    window = Window(stdscr, test_screen_size)
    cursor = Cursor()
    while True:
        window.draw(lines)
        stdscr.move(*cursor.pos())
        key = stdscr.getkey()

        match key.lower():
            case "key_up": cursor.up()
            case "key_down": cursor.down()
            case "key_left": cursor.left()
            case "key_right": cursor.right()
            case "q": return


def make_lines(num_lines):
    result = []
    for i in range(num_lines):
        ch = ascii_lowercase[i % len(ascii_lowercase)]
        result.append(ch + "".join(str(j % 10) for j in range(i)))
    return result    


class Window:
    def __init__(self, screen, size):
        self._screen = screen
        self._nrow = min(size[ROW], curses.LINES) if size else curses.LINES
        self._ncol = min(size[COL], curses.COLS) if size else curses.COLS

    def draw(self, lines):
        self._screen.erase()
        for (y, line) in enumerate(lines):
            if 0 <= y < self._nrow:
                self._screen.addstr(y, 0, line[:self._ncol])

class Cursor:
    def __init__(self):
        self._pos = [0, 0]

    def pos(self):
        return tuple(self._pos)

    def up(self): self._pos[ROW] -= 1

    def down(self): self._pos[ROW] += 1

    def left(self): self._pos[COL] -= 1

    def right(self): self._pos[COL] += 1


if __name__ == '__main__':
    num_lines, logfile = int(sys.argv[1]), sys.argv[2]
    lines = make_lines(num_lines)
    util.open_log(logfile)
    curses.wrapper(lambda stdscr: main(stdscr, lines))
