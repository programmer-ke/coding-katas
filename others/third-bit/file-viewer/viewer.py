import curses
import sys
import util
import string


ROW, COL = 0, 1


def make_lines(num_lines):
    result = []
    for i in range(num_lines):
        ch = string.ascii_lowercase[i % len(string.ascii_lowercase)]
        result.append(ch + "".join(str(j % 10) for j in range(i)))
    return result


class Window:
    def __init__(self, screen, size):
        self._screen = screen
        if size is None:
            self._size = (curses.LINES, curses.COLS)
        else:
            self._size = size

    def size(self):
        return self._size

    def draw(self, lines):
        self._screen.erase()
        for (y, line) in enumerate(lines):
            if 0 <= y < self._size[ROW]:
                self._screen.addstr(y, 0, line[:self._size[COL]])

    def __str__(self):
        return f"Window(S=screen, Z={self._size})"


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

    def insert(self, pos, char):
        assert 0 <= pos[ROW] < self.nrow()
        assert 0 <= pos[COL] <= self.ncol(pos[ROW])
        line = self._lines[pos[ROW]]
        line = line[:pos[COL]] + char + line[pos[COL]:]
        self._lines[pos[ROW]] = line

    def delete(self, pos):
        assert 0 <= pos[ROW] < self.nrow()
        assert 0 <= pos[COL] < self.ncol(pos[ROW])
        line = self._lines[pos[ROW]]
        line = line[:pos[COL]] + line[pos[COL] + 1:]
        self._lines[pos[ROW]] = line
        

class ViewportBuffer(Buffer):
    def __init__(self, lines):
        super().__init__(lines)
        self._top = 0
        self._height = None

    def lines(self):
        return self._lines[self._top:self._bottom()]

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

    INSERTABLE = set(string.ascii_letters + string.digits)

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

    def _get_key(self):
        key = self._screen.getkey()
        if key in self.INSERTABLE:
            return "INSERT", key
        else:
            return None, key

    def _interact(self):
        family, key = self._get_key()
        if family is None:
            name = f"_do_{key}"
            if hasattr(self, name):
                getattr(self, name)()
        else:
            name = f"_do_{family}"
            if hasattr(self, name):
                getattr(self, name)(key)
        self._add_log(key)

    def _add_log(self, key):
        util.LOG.write(f"{key}:{self._cursor.pos()}:\n")

    def _do_DELETE(self):
        self._buffer.delete(self._cursor.pos())

    def _do_INSERT(self, key):
        self._buffer.insert(self._cursor.pos(), key)

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


class HeadlessWindow(Window):
    def __init__(self, screen, size):
        assert size is not None and len(size) == 2
        super().__init__(screen, size)


class HeadlessApp(MainApp):
    def __init__(self, size, lines):
        super().__init__(size, lines)
        self._log = []

    def get_log(self):
        return self._log

    def _add_log(self, key):
        self._log.append((key, self._cursor.pos(), self._screen.display()))

    def _make_window(self):
        self._window = HeadlessWindow(self._screen, self._size)


class HeadlessScreen:
    def __init__(self, size, keystrokes):
        self._size = size
        self._keys = keystrokes
        self._i_key = 0
        self.erase()

    def getkey(self):
        if self._i_key == len(self._keys):
            key = "CONTROL_X"
        else:
            key = self._keys[self._i_key]
            self._i_key += 1
        return key

    def addstr(self, row, col, text):
        assert 0 <= row < self._size[ROW]
        assert col == 0
        assert len(text) <= self._size[COL]
        self._display[row] = text + self._display[row][len(text):]

    def move(self, row, col):
        assert 0 <= row < self._size[ROW]
        assert 0 <= col < self._size[COL]

    def erase(self):
        self._display = ['_' * self._size[COL] for _ in range(self._size[ROW])]

    def display(self):
        return self._display

    def __str__(self):
        return f"Screen(Z={self._size})"


def start():
    num_lines, logfile = int(sys.argv[1]), sys.argv[2]
    size = None
    if len(sys.argv) > 3:
        size = (int(sys.argv[3]), int(sys.argv[4]))
    lines = make_lines(num_lines)
    util.open_log(logfile)
    return size, lines


def make_fixture(keys, size, lines):
    screen = HeadlessScreen(size, keys)
    app = HeadlessApp(size, lines)
    app(screen)
    return app


def test_scroll_down():
    size = (2, 2)
    lines = ["abc", "def", "ghi"]
    keys = ["KEY_DOWN"] * 3
    screen = HeadlessScreen(size, keys)
    app = HeadlessApp(size, lines)
    app(screen)
    assert app.get_log()[-1] == ("CONTROL_X", (2, 0), ["de", "gh"])


def test_delete_middle():
    app = make_fixture(["KEY_RIGHT", "DELETE"], (1, 3), ["abc"])
    assert app.get_log()[-1] == ("CONTROL_X", (0, 1), ["ac_"])


def test_delete_when_impossible():
    try:
        make_fixture(["DELETE"], (1, 1), [""])
    except AssertionError:
        pass


if __name__ == "__main__":
    size, lines = start()
    app = MainApp(size, lines)
    curses.wrapper(app)
