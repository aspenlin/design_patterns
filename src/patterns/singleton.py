"""
Singleton Pattern
- Ensures a class has only one instance and provides global access to it
- Impossible to create a second instance

Drawbacks:
- Whenever something has global access, that thing might change without you knowing it (programming 101: globals are bad)
- Making sure that you only have a single instance is an absurd idea,
  in the future you might need more than one instance (e.g. chatroom)
- Many people argue that you should never use Singleton Pattern

The Singleton Pattern in Python suffers from several drawbacks:
- Singleton Pattern's implementation is difficult to read
- Singleton Pattern makes calls to the class, like Logger(), misleading for readers
- Singleton Pattern forces a design commitment that the Global Object Pattern does not (should prefer use the Global Object Pattern)
- Modules are "singleton" in Python, because import only creates a single copy of each module;
  subsequent imports of the same name keep returning the same module object
"""

# Gang of Four implementation
class Logger(object):

    __instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            print('Creating new instance')
            cls.__instance = cls.__new__(cls)
        return cls.__instance

# More Pythonic implementation
class MorePythonicLogger(object):

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            print('Creating new instance')
            cls.__instance = super(MorePythonicLogger, cls).__new__(cls)
        return cls.__instance

    def __init__(self, a):
        self.__a = a

    def get_a(self):
        return self.__a

class RegionConfig(object):

    __instance = {}
    def __init__(self, region):
        self.__region = region

    @classmethod
    def create_instance(cls, region):
        if region not in cls.__instance:
            cls.__instance[region] = cls(region)
        return cls.__instance[region]


class Main(object):
    """
    $ python src/patterns/singleton.py

    True
    Creating new instance
    <__main__.MorePythonicLogger object at 0x100983cd0>
    1
    <__main__.MorePythonicLogger object at 0x100983cd0>
    2
    2
    Are log1 and log2 the same? True
    """

    def main(self):

        region_conf = RegionConfig.create_instance('US')
        region_conf1 = RegionConfig.create_instance('US')
        print(region_conf is region_conf1)

        log1 = MorePythonicLogger(1)
        print(log1)
        print(log1.get_a())
        log2 = MorePythonicLogger(2)
        print(log2)
        print(log1.get_a())
        print(log2.get_a())
        print('Are log1 and log2 the same?', log1 is log2)

if __name__ == '__main__':
    Main().main()