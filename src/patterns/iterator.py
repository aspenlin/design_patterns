"""
Iterator Pattern
- The Iterator Pattern proposes that the details about how a data structure is traversed should be moved into
  an "iterator" object that, from the outside, simply yields one iterm after another without
  exposing the internals of how the data structure is designed.
- Python supports the Iterator Pattern at the most fundamental level available to a programming language:
  it's built into Python's syntax

Terminology
- An iterator is an object that can be used to loop through collections
- Iterable is an object which can be looped over or iterated over with the help of a loop

OO Principles
- Encapsulate what varies
- Programming to an interface, not an implementation
- Single responsibility principle (separate the collections and the iteration method)

Thoughts:
- I guess we can also say we have a "Comparison Pattern", where the comparison logic is encapsulated.

Refer to: https://python-patterns.guide/gang-of-four/iterator/
"""

class OddNumbers(object):
    """
    An iterable object - the container

    The container must offer an __iter__() method that returns an iterator object.
    Supporting this method makes a container an iterable.
    """
    def __init__(self, maximum):
        self.maximum = maximum

    def __iter__(self):
        return OddIterator(self)

class OddIterator(object):
    """
    An iterator.

    - Each iterator must offer a __next__() method that returns the next item from the container each time it is called.
      It should raise StopIterator when there are no further items.
    - To cover the case that some users pass iterators to a `for` loop instead of passing the underlying container,
      each iterator is required to offer an __iter__() method that simply return itself.
    """
    def __init__(self, container):
        self.__container = container
        self.__n = -1

    def __next__(self):
        self.__n += 2
        if self.__n > self.__container.maximum:
            raise StopIteration
        return self.__n
    def __iter__(self):
        return self

if __name__ == '__main__':
    """
    $ python src/patterns/iterator.py
    =========== Test Iterable ==========
    1
    3
    5
    7
    ============ Iterator returns itself =========
    True
    2
    3
    5
    ========= How Python for loop is implemented ==========
    2
    3
    5
    """
    print('=========== Test Iterable ==========')
    numbers = OddNumbers(7)
    for n in numbers:
        print(n)

    primes = [2, 3, 5]
    print('============ Iterator returns itself =========')
    # Below code handles only a single iterator that we requested ourselves with iter(),
    # both its manual next() calls and its for() loop are all advancing the same iterator along
    # through the 3 items in the underlying list. The for loop works because the iterator object `it` returns itself
    # when asked for its iterator.
    it = iter(primes)
    print(iter(it) is it) # True
    print(next(it))
    for prime in it:
        print(prime)
        break
    print(next(it))

    print('========= How Python for loop is implemented ==========')
    it = iter(primes)
    while True:
        try:
            prime = next(it)
        except StopIteration:
            break
        else:
            print(prime)
