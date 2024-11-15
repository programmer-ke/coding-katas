import curses
import sys
import util
from string import ascii_lowercase

ROW, COL = 0, 1


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

    def size(self):
        return (self._nrow, self._ncol)

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


class ClipCursor(Cursor):
    def __init__(self, buffer, window):
        super().__init__()
        self._buffer = buffer
        self._window = window

    def up(self):
        self._pos[ROW] = max(self._pos[ROW]-1, 0)
        self._fix()

    def down(self):
        self._pos[ROW] = min(self._pos[ROW]+1, self._buffer.nrow()-1)
        self._fix()

    def left(self):
        self._pos[COL] = max(self._pos[COL]-1, 0)
        self._fix()

    def right(self):
        self._pos[COL] = min(
            self._pos[COL]+1,
            self._buffer.ncol(self._pos[ROW])-1
        )
        self._fix()

    def _fix(self):
        self._pos[COL] = min(
            self._pos[COL],
            self._buffer.ncol(self._pos[ROW]) - 1,
            self._window.size()[COL] - 1
        )


class Buffer:
    def __init__(self, lines):
        self._lines = lines[:]

    def lines(self):
        return self._lines

    def nrow(self):
        return len(self._lines)

    def ncol(self, row):
        return len(self._lines[row])


class ViewportBuffer(Buffer):
    def __init__(self, lines):
        super().__init__(lines)
        self._top = 0
        self._height = None

    def lines(self):
        return self._lines[self._top:self._top + self._height]

    def set_height(self, height):
        self._height = height

    def _bottom(self):
        return self._top + self._height

    def transform(self, pos):
        result = (pos[ROW] - self._top, pos[COL])
        return result

    def scroll(self, row, col):
        old = self._top
        if (row == self._top - 1) and self._top > 0:
            self._top -= 1
        elif (row == self._bottom()) and \
             (self._bottom() < self.nrow()):
            self._top += 1


class MainApp:

    TRANSLATE = {
        "\x18": "CONTROL_X",
        'q': "QUIT",
        'Q': "QUIT",
    }

    def __init__(self, size, lines):
        self._size = size
        self._lines = lines
        self._running = True

    def __call__(self, screen):
        self._setup(screen)
        self._run()

    def _setup(self, screen):
        self._screen = screen
        self._make_window()
        self._make_buffer()
        self._make_cursor()

    def _make_window(self):
        self._window = Window(self._screen, self._size)

    def _make_buffer(self):
        self._buffer = ViewportBuffer(self._lines)

    def _make_cursor(self):
        self._cursor = ClipCursor(self._buffer, self._window)

    def _run(self):
        self._buffer.set_height(self._window.size()[ROW])
        while self._running:
            self._window.draw(self._buffer.lines())
            screen_pos = self._buffer.transform(self._cursor.pos())
            self._screen.move(*screen_pos)
            self._interact()
            self._buffer.scroll(*self._cursor.pos())

    def _interact(self):
        key = self._screen.getkey()
        key = self.TRANSLATE.get(key, key)
        name = f"_do_{key}"
        if hasattr(self, name):
            getattr(self, name)()

    def _do_CONTROL_X(self):
        self._running = False

    def _do_KEY_UP(self):
        self._cursor.up()

    def _do_KEY_DOWN(self):
        self._cursor.down()

    def _do_KEY_LEFT(self):
        self._cursor.left()

    def _do_KEY_RIGHT(self):
        self._cursor.right()

    def _do_QUIT(self):
        self._running = False


def start():
    num_lines, logfile = int(sys.argv[1]), sys.argv[2]
    size = None
    if len(sys.argv) > 3:
        size = (int(sys.argv[3]), int(sys.argv[4]))
    lines = make_lines(num_lines)
    util.open_log(logfile)
    return size, lines


if __name__ == "__main__":
    size, lines = start()
    app = MainApp(size, lines)
    curses.wrapper(app)
