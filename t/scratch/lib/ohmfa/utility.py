from urllib.parse import urlparse

class Utility():
    def __init__(self):
        pass
class A:
    def __init__(self, a_value):
        print("Initialize the new instance of A.")
        self.a_value = a_value

class B:
    def __new__(cls, *args, **kwargs):
        return A(42)

    def __init__(self, b_value):
        print("Initialize the new instance of B.")
        self.b_value = b_value

class Rectangle:
    def __init__(self, width, height):
        if not (isinstance(width, (int, float)) and width > 0):
            raise ValueError(f"positive width expected, got {width}")
        self.width = width
        if not (isinstance(height, (int, float)) and height > 0):
            raise ValueError(f"positive height expected, got {height}")
        self.height = height

class Pizza:
    def __init__(self, radius, ingredients):
        self.radius = radius
        self.ingredients = ingredients

    def __repr__(self):
        return (f'Pizza({self.radius!r}, '
                f'{self.ingredients!r})')

    def area(self):
        return self.circle_area(self.radius)

    @staticmethod
    def circle_area(r):
        return r ** 2 * math.pi

    @classmethod
    def margherita(cls):
        return cls(2,['mozzarella', 'tomatoes'])

    @classmethod
    def prosciutto(cls):
        return cls(2,['mozzarella', 'tomatoes', 'ham'])
