import random

class Block:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height


class Row:
    def __init__(self, *children):
        self.children = list(children)

    def get_width(self):
        return sum([c.get_width() for c in self.children])

    def get_height(self):
        return max([c.get_height() for c in self.children], default=0)


class Col:
    def __init__(self, *children):
        self.children = list(children)

    def get_width(self):
        return max([c.get_width() for c in self.children], default=0)

    def get_height(self):
        return sum([c.get_height() for c in self.children])


class PlacedBlock(Block):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.x0 = None
        self.y0 = None

    def place(self, x0, y0):
        self.x0 = x0
        self.y0 = y0

    def report(self):
        return [
            "block",
            self.x0, self.y0,
            self.x0 + self.width, self.y0 + self.height
        ]


class PlacedCol(Col):
    def __init__(self, *children):
        super().__init__(*children)
        self.x0 = None
        self.y0 = None

    def place(self, x0, y0):
        self.x0 = x0
        self.y0 = y0

        y_curr = self.y0
        for child in self.children:
            child.place(self.x0, y_curr)
            y_curr += child.get_height()

    def report(self):
        return [
            "col",
            self.x0, self.y0,
            self.x0 + self.get_width(), self.y0 + self.get_height()
        ] + [child.report() for child in self.children]


class PlacedRow(Row):
    def __init__(self, *children):
        super().__init__(*children)
        self.x0 = None
        self.y0 = None

    def place(self, x0, y0):
        self.x0 = x0
        self.y0 = y0

        y1 = self.y0 + self.get_height()
        x_curr = self.x0
        for child in self.children:
            child_y = y1 - child.get_height()
            child.place(x_curr, child_y)
            x_curr += child.get_width()

    def report(self):
        return [
            "row",
            self.x0, self.y0,
            self.x0 + self.get_width(), self.y0 + self.get_height()
        ] + [child.report() for child in self.children]


def make_screen(width, height):
    screen = []
    for i in range(height):
        screen.append([" "] * width)
    return screen


def draw(screen, node, fill=None):
    fill = next_fill(fill)
    node.render(screen, fill)
    if hasattr(node, 'children'):
        for child in node.children:
            fill = draw(screen, child, fill)
    return fill


def next_fill(fill):
    return "a" if fill is None else chr(ord(fill) + 1)


class Renderable:
    def render(self, screen, fill):
        for ix in range(self.get_width()):
            for iy in range(self.get_height()):
                screen[self.y0 + iy][self.x0 + ix] = fill


class RenderedBlock(Renderable, PlacedBlock):
    pass


class RenderedCol(Renderable, PlacedCol):
    pass


class RenderedRow(Renderable, PlacedRow):
    pass


class WrappedBlock(RenderedBlock):
    def wrap(self):
        return self


class WrappedCol(RenderedCol):
    def wrap(self):
        return RenderedCol(*[c.wrap() for c in self.children])


class WrappedRow(RenderedRow):
    def __init__(self, width, *children):
        super().__init__(*children)
        assert width >= 0, "Non-negative width is required"
        self.width = width

    def get_width(self):
        return self.width

    def wrap(self):
        children = [c.wrap() for c in self.children]
        rows = self._bucket(children)
        new_rows = [RenderedRow(*r) for r in rows]
        new_col = RenderedCol(*new_rows)
        return RenderedRow(new_col)

    def _bucket(self, children):
        result = []
        current_row = []
        current_x = 0

        for child in children:
            child_width = child.get_width()
            if current_x + child_width <= self.width:
                current_row.append(child)
                current_x += child_width
            else:
                result.append(current_row)
                current_row = [child]
                current_x = child_width
        result.append(current_row)
        return result
        

def render(block):
    screen = make_screen(block.get_width(), block.get_height())
    draw(screen, block)
    row_chars = ["".join(row) for row in screen]
    return "\n".join(row_chars)

def test_wrap_a_row_of_two_blocks_that_do_not_fit_on_one_row():
    fixture = WrappedRow(3, WrappedBlock(2, 1), WrappedBlock(2, 1))
    wrapped = fixture.wrap()
    wrapped.place(0, 0)
    assert wrapped.report() == [
        "row",
        0, 0, 2, 2,
        [
            "col",
            0, 0, 2, 2,
            ["row", 0, 0, 2, 1, ["block", 0, 0, 2, 1]],
            ["row", 0, 1, 2, 2, ["block", 0, 1, 2, 2]],
        ],
    ]


def test_renders_a_column_of_two_blocks():
    fixture = RenderedCol(RenderedBlock(1, 1), RenderedBlock(2, 4))
    fixture.place(0, 0)

    expected = "\n".join(["ba", "cc", "cc", "cc", "cc"])
    assert render(fixture) == expected


def test_lays_out_a_grid_of_rows_of_columns():
    fixture = Col(
        Row(Block(1, 2), Block(3, 4)),
        Row(Block(5, 6), Col(Block(7, 8), Block(9, 10)))
    )
    assert fixture.get_width() == 14
    assert fixture.get_height() == 22


def test_places_a_column_of_two_blocks():
    fixture = PlacedCol(PlacedBlock(1, 1), PlacedBlock(2, 4))
    fixture.place(0, 0)
    assert fixture.report() == [
        "col",
        0, 0, 2, 5,
        ["block", 0, 0, 1, 1],
        ["block", 0, 1, 2, 5],
    ]


def test():
    for k, value in globals().items():
        if k.startswith('test_'):
            value()

def render_example():
    parent_width = random.randint(20, 80)
    no_children = random.randint(2, 20)
    children = [
        WrappedBlock(random.randint(1, parent_width), random.randint(1, 20)) for _ in range(no_children)
    ]
    fixture = WrappedRow(parent_width, *children)
    
    # fixture = WrappedRow(20, WrappedBlock(15, 10), WrappedBlock(10, 10))
    wrapped = fixture.wrap()
    wrapped.place(0, 0)
    result = render(wrapped)
    print(result)
    

if __name__ == "__main__":
    test()
    render_example()
