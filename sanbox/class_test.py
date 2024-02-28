class Base:
    def __init__(self):
        self.a = "test"
        self._b = "test2"
        self.__c = "test3"

class Derived(Base):
    def __init__(self):
        Base.__init__(self)
        print("calling base")
        print(self.__c)

test1 = Base()
print(test1.a)

test2 = Derived() # self.__c will return an error as it is private
