"""
The essence of Strategy Pattern is - using composition instead of inheritance, because inheritance is not intended for code reuse.
- The Strategy Pattern defines a family of algorithms, encapsulates each one of them, and makes them interchangeable.
  Strategy lets the algorithms vary independently from the clients that use it
  (decouple the algorithm from the clients that use them).
"""
from abc import ABC
from abc import abstractmethod

# Below is bad design pattern using inheritance
class AbsBadDuck(object):

    @abstractmethod
    def quack(self):
        pass

    @abstractmethod
    def fly(self):
        pass

class BadCityDuck(AbsBadDuck):

    def quack(self):
        print('<< Silence >>')

    def fly(self):
        print('Cannot fly')

class BadWildDuck(AbsBadDuck):

    def quack(self):
        print('quack')

    def fly(self):
        print('Can fly')

class BadMountDuck(AbsBadDuck):

    def quack(self):
        print('<< Silence >>')

    def fly(self):
        print('Can fly')

# Below is the correct design pattern using Strategy Pattern

class AbsFlyBehavior(ABC):

    @abstractmethod
    def perform_fly(self):
        pass

class CanFly(AbsFlyBehavior):

    def perform_fly(self):
        print('Can fly')

class CannotFly(AbsFlyBehavior):

    def perform_fly(self):
        print('Cannot fly')

class AbsQuackBehavior(ABC):

    @abstractmethod
    def perform_quack(self):
        pass

class Quack(AbsQuackBehavior):

    def perform_quack(self):
        print('quack')

class MuteQuack(AbsQuackBehavior):

    def perform_quack(self):
        print('<< Silence >>')

class AbsDuck(ABC):

    def __int__(self, fly_behavior, quack_behavior):
        assert isinstance(fly_behavior, AbsFlyBehavior)
        assert isinstance(quack_behavior, AbsQuackBehavior)
        self.__fly_behavior = fly_behavior
        self.__quack_behavior = quack_behavior

    def fly(self):
        self.__fly_behavior.perform_fly()

    def quack(self):
        self.__quack_behavior.perform_quack()

    def swim(self):
        print('All ducks swim!')

class CityDuck(AbsDuck):

    def __int__(self):
        super().__int__(CannotFly(), MuteQuack())

    def dispaly(self):
        print('I am a city duck')


class WildDuck(AbsDuck):

    def __int__(self):
        super().__int__(CanFly(), Quack())


class MountDuck(AbsDuck):

    def __int__(self):
        super().__int__(CanFly(), MuteQuack())


# Below is a more concrete Strategy Pattern example
class AbsDataReader(ABC):

    @abstractmethod
    def read(self):
        pass

class AbsDataFixer(ABC):

    @abstractmethod
    def fix(self):
        pass

class AbsDataSaver(ABC):

    @abstractmethod
    def save(self):
        pass

class AbsDataBuilder(ABC):

    def __int__(self, data_reader, data_fixer, data_saver):
        assert isinstance(data_reader, AbsDataReader)
        assert isinstance(data_fixer, AbsDataFixer)
        assert isinstance(data_saver, AbsDataSaver)
        self.__data_reader = data_reader
        self.__data_fixer = data_fixer
        self.__data_saver = data_saver

    def build(self):
        raw_data = self.__data_reader.read()
        fixed_data = self.__data_fixer.fix()
        self.__data_saver.save()

# Questions:
# - Should we always honor Strategy Pattern? Or only when the same strategy can be used by multiple clients?
#   What if every data needs to be fixed in different ways? Should we do the following instead?

class AbsDataBuilder1(ABC):

    def __int__(self, data_reader, data_saver):
        assert isinstance(data_reader, AbsDataReader)
        assert isinstance(data_saver, AbsDataSaver)
        self.__data_reader = data_reader
        self.__data_saver = data_saver

    def build(self):
        raw_data = self.__data_reader.read()
        fixed_data = self.fix()
        self.__data_saver.save()

    @abstractmethod
    def fix(self):
        pass

class SimpleDataBuilder(AbsDataBuilder1):

    def __int__(self):
        super().__int__(...)

    def fix(self):
        print('Perform some simple fix')


class ComplexDataBuilder(AbsDataBuilder1):

    def __int__(self):
        super().__int__(...)

    def fix(self):
        print('Perform some complex fix')