"""
State Pattern

The State Pattern allows an object (GumballMachine below) to alter its behavior when its internal state changes
(e.g. change from NoQuarterState to HasQuarterState). The object will appear to change its class.

With State Pattern, we have a set of behaviors encapsulated in state objects;
at any time the context is delegating to one of those states.

Think of the State Pattern as an alternative to putting lots of conditionals in your context;
by encapsulating the behaviors within state object, you can simply change the state object in context to change its behavior.

OO Principle
- Encapsulate what varies
"""
from abc import ABC, abstractmethod
from enum import Enum
import numpy as np

class GumballState(Enum):

    SOLD_OUT = 0
    NO_QUARTER = 1
    HAS_QUARTER = 2
    SOLD = 3

class AbsGumballMachine(ABC):

    @abstractmethod
    def insert_quarter(self):
        pass

    @abstractmethod
    def eject_quarter(self):
        pass

    @abstractmethod
    def turn_crank(self):
        pass


class MessyGumballMachine(AbsGumballMachine):
    """
    How to implement one in ten get a free gumball?
    - You have to add a new conditional in every single method to handle the WINNER state
    - turn_crank will be especially messy, because you have to add code to check whether you've got a winner
      and then switch to either the WINNER or the SOLD state
    """

    def __init__(self, count):
        self.__count = count
        self.__state = GumballState.SOLD_OUT
        if self.__count > 0:
            self.__state = GumballState.NO_QUARTER

    def insert_quarter(self):
        if self.__state == GumballState.HAS_QUARTER:
            print('There is already a quarter. You cannot insert another')
        elif self.__state == GumballState.NO_QUARTER:
            self.__state = GumballState.HAS_QUARTER
            print('You inserted a quarter')
        elif self.__state == GumballState.SOLD_OUT:
            print('You cannot insert a quarter, the machine is sold out.')
        elif self.__state == GumballState.SOLD:
            print('Please wait, we are already giving you a gumball')

    def eject_quarter(self):
        if self.__state == GumballState.HAS_QUARTER:
            print('Quarter returned')
            self.__state = GumballState.NO_QUARTER
        elif self.__state == GumballState.NO_QUARTER:
            print('You have not inserted a quarter')
        elif self.__state == GumballState.SOLD_OUT:
            print('You cannot eject, you have not inserted a quarter yet.')
        elif self.__state == GumballState.SOLD:
            print('Sorry, you already turned the crank')

    def turn_crank(self):
        if self.__state == GumballState.HAS_QUARTER:
            print('You turned...')
            self.__state = GumballState.SOLD
        elif self.__state == GumballState.NO_QUARTER:
            print('You turned, but there is no quarter')
        elif self.__state == GumballState.SOLD_OUT:
            print('You turned, but there are no gumballs')
        elif self.__state == GumballState.SOLD:
            print('Turning twice does not give you another gumball')

    def dispense(self):
        if self.__state == GumballState.HAS_QUARTER:
            print('No gumball dispensed')
        elif self.__state == GumballState.NO_QUARTER:
            print('You need to pay first')
        elif self.__state == GumballState.SOLD_OUT:
            print('No gumball dispensed')
        elif self.__state == GumballState.SOLD:
            print('A gumball comes rolling out the slot...')
            self.__count -= 1
            if self.__count == 0:
                print('Oops, out of gumball')
                self.__state = GumballState.SOLD_OUT
            else:
                self.__state = GumballState.NO_QUARTER

class GumballMachine(AbsGumballMachine):
    """
    - Localized the behavior of each state into its own class
    - Removed all the troublesome if statements that would have been difficult to maintain
    - Closed each state for modification, and yet left the GumballMachine open to extension by adding new state classes
    - Easier to read and understand
    - The downside is that we now have a lot of state classes; but this is a price we have to pay for flexibility;
      the good thing is these classes are not exposed to clients and we avoid the conditional statements.
    """

    def __init__(self, num_gumball):
        self.__sold_out_state = SoldOutState(self)
        self.__no_quarter_state = NoQuarterState(self)
        self.__has_quarter_state = HasQuarterState(self)
        self.__sold_state = SoldState(self)
        self.__winner_state = WinnerState(self)

        self.__count = num_gumball
        self.__state = None
        if self.__count > 0:
            self.__state = self.__no_quarter_state
        else:
            self.__state = self.__sold_out_state

    def __str__(self):
        return f'************** Gumball machine with {self.__count} gumballs left ******************'

    def insert_quarter(self):
        self.__state.insert_quarter()

    def eject_quarter(self):
        self.__state.eject_quarter()

    def turn_crank(self):
        self.__state.turn_crank()
        self.__state.dispense()

    def set_state(self, state):
        self.__state = state

    def release_ball(self):
        """
        This public method is a bit strange to me. Can you call this method at any time?
        """
        print('A gumball comes rolling out the slot...')
        if self.__count > 0:
            self.__count -= 1

    def get_has_quarter_state(self):
        return self.__has_quarter_state

    def get_no_quarter_state(self):
        return self.__no_quarter_state

    def get_sold_state(self):
        return self.__sold_state

    def get_sold_out_state(self):
        return self.__sold_out_state

    def get_winner_state(self):
        return self.__winner_state

    def get_count(self):
        return self.__count

class AbsState(ABC):

    @abstractmethod
    def insert_quarter(self):
        pass

    @abstractmethod
    def eject_quarter(self):
        pass

    @abstractmethod
    def turn_crank(self):
        pass

    @abstractmethod
    def dispense(self):
        pass

class NoQuarterState(AbsState):

    def __init__(self, gumball_machine):
        self.__gumball_machine = gumball_machine

    def insert_quarter(self):
        print('You inserted a quarter')
        self.__gumball_machine.set_state(self.__gumball_machine.get_has_quarter_state())

    def eject_quarter(self):
        print('You have not inserted a quarter')

    def turn_crank(self):
        print('You turned, but there is no quarter')

    def dispense(self):
        print('You need to pay first')

class HasQuarterState(AbsState):

    def __init__(self, gumball_machine):
        self.__gumball_machine = gumball_machine
        np.random.seed(0)

    def insert_quarter(self):
        print('There is already a quarter. You cannot insert another')

    def eject_quarter(self):
        print('Quarter returned')
        self.__gumball_machine.set_state(self.__gumball_machine.get_no_quarter_state())

    def turn_crank(self):
        print('You turned...')
        winner = np.random.randint(10)
        if winner == 0 and self.__gumball_machine.get_count() > 1:
            self.__gumball_machine.set_state(self.__gumball_machine.get_winner_state())
        else:
            self.__gumball_machine.set_state(self.__gumball_machine.get_sold_state())

    def dispense(self):
        print('No gumball dispensed')

class SoldState(AbsState):

    def __init__(self, gumball_machine):
        self.__gumball_machine = gumball_machine

    def insert_quarter(self):
        print('Please wait, we are already giving you a gumball')

    def eject_quarter(self):
        print('Sorry, you already turned the crank')

    def turn_crank(self):
        print('Turning twice does not give you another gumball')

    def dispense(self):
        self.__gumball_machine.release_ball()
        if self.__gumball_machine.get_count() > 0:
            self.__gumball_machine.set_state(self.__gumball_machine.get_no_quarter_state())
        else:
            print('Oops, out of gumball')
            self.__gumball_machine.set_state(self.__gumball_machine.get_sold_out_state())

class SoldOutState(AbsState):

    def __init__(self, gumball_machine):
        self.__gumball_machine = gumball_machine

    def insert_quarter(self):
        print('You cannot insert a quarter, the machine is sold out.')

    def eject_quarter(self):
        print('You cannot eject, you have not inserted a quarter yet.')

    def turn_crank(self):
        print('You turned, but there are no gumballs')

    def dispense(self):
        print('No gumball dispensed')

class WinnerState(SoldState):

    def __init__(self, gumball_machine):
        self.__gumball_machine = gumball_machine

    def insert_quarter(self):
        print('Please wait, we are already giving you a gumball')

    def eject_quarter(self):
        print('Sorry, you already turned the crank')

    def turn_crank(self):
        print('Turning twice does not give you another gumball')

    def dispense(self):
        """
        Dispense twice when gumball machine has enough gumballs.
        """
        self.__gumball_machine.release_ball()
        if self.__gumball_machine.get_count() == 0:
            self.__gumball_machine.set_state(self.__gumball_machine.get_sold_out_state())
        else:
            self.__gumball_machine.release_ball()
            print('You are a winner. You got two gumballs for your quarter')
            if self.__gumball_machine.get_count() > 0:
                self.__gumball_machine.set_state(self.__gumball_machine.get_no_quarter_state())
            else:
                print('Oops, out of gumball')
                self.__gumball_machine.set_state(self.__gumball_machine.get_sold_out_state())



if __name__ == '__main__':
    gumball_machine = GumballMachine(5)
    print(gumball_machine)
    gumball_machine.insert_quarter()
    gumball_machine.turn_crank()
    print(gumball_machine)
    gumball_machine.insert_quarter()
    gumball_machine.turn_crank()
    print(gumball_machine)
    gumball_machine.insert_quarter()
    gumball_machine.turn_crank()


