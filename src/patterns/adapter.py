"""
Adapter Pattern
- Converts the interface of a class into another interface that the clients expect.
  Lets classes work together that couldn't otherwise because of the incompatible interfaces.
- Decouples the clients from the implemented interfaces
"""
from abc import ABC, abstractmethod
class AbsDuck(ABC):

    @abstractmethod
    def quack(self):
        pass

    @abstractmethod
    def fly(self):
        pass

class Turkey(object):

    def gobble(self):
        print('I am goggling')

    def fly(self):
        print('I am flying')

class TurkeyToDuckAdapter(AbsDuck):
    """
    Wrap a turkey into a duck
    """

    def __init__(self, turkey):
        assert isinstance(turkey, Turkey)
        self.__turkey = turkey

    def quack(self):
        self.__turkey.gobble()

    def fly(self):
        for _ in range(5):
            self.__turkey.fly()

class Main(object):
    """
    $ python src/patterns/adapter.py
    """

    def main(self):
        turkey = Turkey()
        turkey_to_duck = TurkeyToDuckAdapter(turkey)
        turkey_to_duck.quack()
        turkey_to_duck.fly()

if __name__ == '__main__':
    Main().main()
