
class Triangle:
    def __init__(self, a, b, c, perimeter=None):
        self.a = a
        self.b = b
        self.c = c
        if perimeter:
            self._perimeter = perimeter
        else:
            self._perimeter = a + b + c
    def is_equilateral(self):  #self: iNstance of obj  INSTANCE METHOD
        answer = False
        if (self.a == self.b) and (self.a == self.c):
            answer = True
        return answer

    @staticmethod # STATIC METHOD
    def perimeter(triangle):
        return triangle.a + triangle.b + triangle.c

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, a):
        self._a = a


triangle = Triangle(3, 4, 5)
print("triangle.a ->", triangle.a)
triangle.a = 9
print("triangle.a ->", triangle.a)
print("triangle is_equilateral ->", triangle.is_equilateral())
triangle.d = 5

triangle1 = Triangle(3,4,5)
triangle2 = Triangle(1,2,3)
print("triangle1 is_equilateral -> ", triangle1.is_equilateral())
print("perimeter triangle1 ->", Triangle.perimeter(triangle1))
print("perimeter triangle2 ->", Triangle.perimeter(triangle2))

"""""
class Triangle:
    def __init__(self, a, b, c):
        self._a = a
        self._b = b
        self._c = c
    @property
    def a(self):
        return self._a
    @a.setter
    def a(self, a):
      self._a = a
    @property
    def b(self):
        return self._b
    @property
    def c(self):
        return self._c

triangle = Triangle(3, 4, 5)
# triangle.b = 8
triangle.c = 8
"""""



"""""
def funct(a,b=[]): # mutable obj -> not good choice
    return a+b

# string immutable, change the address
a = 'hello'
b = a+' world'
# a = hello

a = [1] # mutable
b = a
b.append(2)
a
# a = [1,2]
"""""
