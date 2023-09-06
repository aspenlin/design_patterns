"""
A compound pattern combines two or more patterns into a solution that solves a recurring or general problem.

Below is not a compound pattern, it is just a set of patterns working together.
"""
from abc import ABC, abstractmethod

class AbsQuackObservable(ABC):

    @abstractmethod
    def register_observer(self, observer):
        pass

    @abstractmethod
    def notify_observer(self):
        pass

class AbsQuackable(AbsQuackObservable):

    @abstractmethod
    def quack(self):
        pass

class MallardDuck(AbsQuackable):

    def __init__(self):
        self.__observable = Observable(self)

    def __str__(self):
        return 'Mallard Duck'

    def quack(self):
        print('Quack')
        self.notify_observer()

    def register_observer(self, observer):
        self.__observable.register_observer(observer)

    def notify_observer(self):
        self.__observable.notify_observer()

class RedHeadDuck(AbsQuackable):

    def __init__(self):
        self.__observable = Observable(self)

    def __str__(self):
        return 'Red Head Duck'

    def quack(self):
        print('Quack')
        self.notify_observer()

    def register_observer(self, observer):
        self.__observable.register_observer(observer)

    def notify_observer(self):
        self.__observable.notify_observer()

class DuckCall(AbsQuackable):

    def __init__(self):
        self.__observable = Observable(self)

    def __str__(self):
        return 'Duck Call'

    def quack(self):
        print('Kwak')
        self.notify_observer()

    def register_observer(self, observer):
        self.__observable.register_observer(observer)

    def notify_observer(self):
        self.__observable.notify_observer()

class RubberDuck(AbsQuackable):

    def __init__(self):
        self.__observable = Observable(self)

    def __str__(self):
        return 'Rubber Duck'

    def quack(self):
        print('Squeak')
        self.notify_observer()

    def register_observer(self, observer):
        self.__observable.register_observer(observer)

    def notify_observer(self):
        self.__observable.notify_observer()

class Goose(object):

    def honk(self):
        print('Honk')

# Adapter Pattern
# adapt a goose to a duck
class GooseAdapter(AbsQuackable):

    def __init__(self, goose):
        assert isinstance(goose, Goose)
        self.__observable = Observable(self)
        self.__goose = goose

    def __str__(self):
        return 'Goose pretending to be a Duck'

    def quack(self):
        self.__goose.honk()
        self.notify_observer()

    def register_observer(self, observer):
        self.__observable.register_observer(observer)

    def notify_observer(self):
        self.__observable.notify_observer()

# Decorator Pattern
# give the ducks some new behavior by wrapping them with a decorator object
NUM_QUACKS = 0
class QuackCounter(AbsQuackable):

    def __init__(self, duck):
        assert isinstance(duck, AbsQuackable)
        self.__duck = duck

    def quack(self):
        self.__duck.quack()
        global NUM_QUACKS
        NUM_QUACKS += 1

    @classmethod
    def get_quacks(cls):
        return NUM_QUACKS

    def register_observer(self, observer):
        self.__duck.register_observer(observer)

    def notify_observer(self):
        pass

# Factory Pattern
# create a polymorphic method that takes a factory and uses it to create objects.
# By passing in different factories, we get to use different product families in the method.
class AbstractDuckFactory(ABC):

    @abstractmethod
    def create_MallardDuck(self):
        pass

    @abstractmethod
    def create_RedHeadDuck(self):
        pass

    @abstractmethod
    def create_DuckCall(self):
        pass

    @abstractmethod
    def create_RubberDuck(self):
        pass

class DuckFactory(AbstractDuckFactory):

    def create_MallardDuck(self):
        return MallardDuck()

    def create_RedHeadDuck(self):
        return RedHeadDuck()

    def create_DuckCall(self):
        return DuckCall()

    def create_RubberDuck(self):
        return RubberDuck()

class CountingDuckFactory(AbstractDuckFactory):

    def create_MallardDuck(self):
        return QuackCounter(MallardDuck())

    def create_RedHeadDuck(self):
        return QuackCounter(RedHeadDuck())

    def create_DuckCall(self):
        return QuackCounter(DuckCall())

    def create_RubberDuck(self):
        return QuackCounter(RubberDuck())

# Composite and Iterator Pattern
# Allow us to treat a collections of objects in the same way as individual objects
class Flock(AbsQuackable):

    def __init__(self):
        super().__init__()
        self.__quackers = []

    def add(self, quacker):
        assert isinstance(quacker, AbsQuackable)
        self.__quackers.append(quacker)

    def quack(self):
        for quacker in self.__quackers:
            quacker.quack()

    def register_observer(self, observer):
        for quacker in self.__quackers:
            quacker.register_observer(observer)

    def notify_observer(self):
        pass

# Observer Pattern
class Observable(AbsQuackObservable):

    def __init__(self, duck):
        assert isinstance(duck, AbsQuackObservable)
        self.__observers = []
        self.__duck = duck

    def register_observer(self, observer):
        assert isinstance(observer, AbsObserver)
        self.__observers.append(observer)

    def notify_observer(self):
        for observer in self.__observers:
            observer.update(self.__duck)

class AbsObserver(ABC):

    @abstractmethod
    def update(self, duck):
        pass


class Quackologist(AbsObserver):

    def update(self, duck):
        assert isinstance(duck, AbsQuackObservable)
        print(f'Quackologist: {duck} just quacked')

if __name__ == '__main__':

    def simulate(duck):
        assert isinstance(duck, AbsQuackable)
        duck.quack()

    duck_factory = CountingDuckFactory()
    red_head_duck = duck_factory.create_RedHeadDuck()
    duck_call = duck_factory.create_DuckCall()
    rubber_duck = duck_factory.create_RubberDuck()
    goose_duck = GooseAdapter(Goose())
    print('Duck Simulator: With Observer')

    flock_of_ducks = Flock()
    flock_of_ducks.add(red_head_duck)
    flock_of_ducks.add(duck_call)
    flock_of_ducks.add(rubber_duck)
    flock_of_ducks.add(goose_duck)

    flock_of_mallards = Flock()
    mallard_one = duck_factory.create_MallardDuck()
    mallard_two = duck_factory.create_MallardDuck()
    mallard_three = duck_factory.create_MallardDuck()
    mallard_four = duck_factory.create_MallardDuck()
    flock_of_mallards.add(mallard_one)
    flock_of_mallards.add(mallard_two)
    flock_of_mallards.add(mallard_three)
    flock_of_mallards.add(mallard_four)

    flock_of_ducks.add(flock_of_mallards)

    quackologist = Quackologist()
    flock_of_ducks.register_observer(quackologist)

    simulate(flock_of_ducks)
    print(f'The ducks quacked {QuackCounter.get_quacks()} times')

