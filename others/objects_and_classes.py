"""Implementing an object system"""

import math


class Shape:
    def __init__(self, name):
        self.name = name

    def perimeter(self):
        raise NotImplementedError("perimeter")

    def area(self):
        raise NotImplementedError("area")


class Square(Shape):
    def __init__(self, name, side):
        super().__init__(name)
        self.side = side

    def perimeter(self):
        return 4 * self.side

    def area(self):
        return self.side**2


class Circle(Shape):
    def __init__(self, name, radius):
        super().__init__(name)
        self.radius = radius

    def perimeter(self):
        return 2 * math.pi * self.radius

    def area(self):
        return math.pi * self.radius**2


examples = [Square("sq", 3), Circle("ci", 2)]
for thing in examples:
    n = thing.name
    p = thing.perimeter()
    a = thing.area()
    print(f"{n} has perimeter {p:.2f} and area {a:.2f}")


# dict examples
# square
def square_area(thing):
    return thing["side"] ** 2


def square_perimeter(thing):
    return thing["side"] * 4


def square_new(name, side):
    return {
        "name": name,
        "side": side,
        "perimeter": square_perimeter,
        "area": square_area,
    }


# circle
def circle_area(thing):
    return math.pi * thing["radius"] ** 2


def circle_perimeter(thing):
    return 2 * math.pi * thing["radius"]


def circle_new(name, radius):
    return {
        "name": name,
        "radius": radius,
        "perimeter": circle_perimeter,
        "area": circle_area,
    }


def call(thing, method_name):
    return thing[method_name](thing)


for ex in [square_new("sq", 3), circle_new("ci", 2)]:
    name = ex["name"]
    perimeter = call(ex, "perimeter")
    area = call(ex, "area")
    print(f"{name} {perimeter:.2f} {area:.2f}")

# introducing classes
Square = {"perimeter": square_perimeter, "area": square_area, "_classname": "Square"}

Circle = {"perimeter": circle_perimeter, "area": circle_area, "_classname": "Circle"}


def square_new(name, side):
    return {"name": name, "side": side, "_class": Square}


def circle_new(name, radius):
    return {"name": name, "radius": radius, "_class": Circle}


def call(thing, method_name):
    return thing["_class"][method_name](thing)


for ex in [square_new("sq", 3), circle_new("ci", 2)]:
    name = ex["name"]
    perimeter = call(ex, "perimeter")
    area = call(ex, "area")
    print(f"{name} {perimeter:.2f} {area:.2f}")


# extra arguments
def square_larger(thing, size):
    return call(thing, "area") > size


def circle_larger(thing, size):
    return call(thing, "area") > size


Square = {
    "perimeter": square_perimeter,
    "area": square_area,
    "larger": square_larger,
    "_classname": "Square",
}

Circle = {
    "perimeter": circle_perimeter,
    "area": circle_area,
    "larger": circle_larger,
    "_classname": "Circle",
}


def call(thing, method_name, *args):
    return thing["_class"][method_name](thing, *args)


examples = [square_new("sq", 3), circle_new("ci", 2)]
for ex in examples:
    result = call(ex, "larger", 10)
    print(f"is {ex['name']} larger? {result}")


# inheritance
class Shape:
    def __init__(self, name):
        self.name = name

    def perimeter(self):
        raise NotImplementedError("perimeter")

    def area(self):
        raise NotImplementedError("area")

    def density(self, weight):
        return weight / self.area()


class Square(Shape):
    def __init__(self, name, side):
        super().__init__(name)
        self.side = side

    def perimeter(self):
        return 4 * self.side

    def area(self):
        return self.side**2


class Circle(Shape):
    def __init__(self, name, radius):
        super().__init__(name)
        self.radius = radius

    def perimeter(self):
        return 2 * math.pi * self.radius

    def area(self):
        return math.pi * self.radius**2


examples = [Square("sq", 3), Circle("ci", 2)]
for ex in examples:
    n = ex.name
    d = ex.density(5)
    print(f"{n} density: {d:.2f}")


def shape_density(thing, weight):
    return weight / call(thing, "area")


Shape = {"density": shape_density, "_classname": "Shape", "_parent": None}


Square = {
    "perimeter": square_perimeter,
    "area": square_area,
    "larger": square_larger,
    "_classname": "Square",
    "_parent": Shape,
}

Circle = {
    "perimeter": circle_perimeter,
    "area": circle_area,
    "larger": circle_larger,
    "_classname": "Circle",
    "_parent": Shape,
}


def call(thing, method_name, *args):
    method = find(thing["_class"], method_name)
    return method(thing, *args)


def find(cls, method_name):
    while cls is not None:
        if method_name in cls:
            return cls[method_name]
        cls = cls["_parent"]
    raise NotImplementedError(method_name)


examples = [square_new("sq", 3), circle_new("ci", 2)]
for ex in examples:
    n = ex["name"]
    d = call(ex, "density", 5)
    print(f"{n} density: {d:.2f}")

# call(ex, "volume")

# constructors


def shape_new(name):
    return {"name": name, "_class": Shape}


Shape = {
    "density": shape_density,
    "_classname": "Shape",
    "_parent": None,
    "_new": shape_new,
}


def make(cls, *args):
    return cls["_new"](*args)


def square_new(name, side):
    return make(Square["_parent"], name) | {"side": side, "_class": Square}


Square = {
    "perimeter": square_perimeter,
    "area": square_area,
    "larger": square_larger,
    "_classname": "Square",
    "_parent": Shape,
    "_new": square_new,
}


def circle_new(name, radius):
    return make(Shape, name) | {"radius": radius, "_class": Circle}


Circle = {
    "perimeter": circle_perimeter,
    "area": circle_area,
    "larger": circle_larger,
    "_classname": "Circle",
    "_parent": Shape,
    "_new": circle_new,
}

examples = [make(Square, "sq", 3), make(Circle, "ci", 2)]
for ex in examples:
    n = ex["name"]
    d = call(ex, "density", 5)
    print(f"{n}: {d:.2f}")
