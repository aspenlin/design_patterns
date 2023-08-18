"""
Command Pattern
- Encapsulate a request as an object, thereby letting you parameterize other objects with different requests,
  queue, or log requests, and support undo-able operations
1) It is the request ("command") that we are encapsulating
2) The Command Pattern decouples an object making a request from the one that knows how to perform it
   A Command object is at the center of this decoupling

Related OO Principles
- Encapsulate what varies
- Strive for loosely coupled designs between objects that interacts
- Classes should be open for extension but closed for modification
- Depend on abstraction. Do not depend on concrete classes.
-
"""
from abc import ABC, abstractmethod

class AbsCommand(ABC):

    @abstractmethod
    def execute(self):
        """
        Action
        """

    def unexecute(self):
        """
        Undo
        """

class NullCommand(AbsCommand):
    """
    A null command that does not do anything.
    """

    def execute(self):
        """
        do nothing
        """
        return

    def unexecute(self):
        """
        do nothing
        """
        return

class Light(object):
    """
    A light that can turn on and off.
    """

    def __init__(self, location):
        self.__location = location

    def on(self):
        print(f'{self.__location} light is on')

    def off(self):
        print(f'{self.__location} light  is off')

class LightOnCommand(AbsCommand):
    """
    Command to turn light on.
    """

    def __init__(self, light):
        self.__light = light

    def execute(self):
        self.__light.on()

    def unexecute(self):
        self.__light.off()

class LightOffCommand(AbsCommand):
    """
    Command to turn light off.
    """

    def __init__(self, light):
        self.__light = light

    def execute(self):
        self.__light.off()

    def unexecute(self):
        self.__light.on()

class MacroCommand(AbsCommand):
    """
    A macro command that encapsulates multiple commands.
    """

    def __init__(self, cmd_list):
        for cmd in cmd_list:
            assert isinstance(cmd, AbsCommand)
        self.__cmd_list = cmd_list

    def execute(self):
        for cmd in self.__cmd_list:
            cmd.execute()

    def unexecute(self):
        for cmd in self.__cmd_list:
            cmd.unexecute()



class RemoteControl(object):
    """
    The remote control here has n slots. Each slot has an on button and an off button.
    Each button is loaded with a command (request)
    When any of the button is pressed, its relating command will execute.

    The remote control does not have any idea what the request is,
    it just has a command object that knows how to talk to the right object to get the work done.
    The remote control is decoupled from the receivers.
    """

    def __init__(self, n_slots):
        # Initialize to null commands.
        self.__on_cmds = [NullCommand() for _ in range(n_slots)]
        self.__off_cmds = [NullCommand() for _ in range(n_slots)]
        self.__last_cmd = NullCommand()

    def set_command(self, idx, on_cmd, off_cmd):
        # The remote does not care what command object has, as long as it implements the AbsCommand interface
        assert isinstance(on_cmd, AbsCommand)
        assert isinstance(off_cmd, AbsCommand)
        assert 0 <= idx < len(self.__on_cmds)
        self.__on_cmds[idx] = on_cmd
        self.__off_cmds[idx] = off_cmd

    def click_on(self, idx):
        print(f'Clicking slot {idx} on button...')
        self.__on_cmds[idx].execute()
        self.__last_cmd = self.__on_cmds[idx]

    def click_off(self, idx):
        print(f'Clicking slot {idx} off button...')
        self.__off_cmds[idx].execute()
        self.__last_cmd = self.__off_cmds[idx]

    def undo(self):
        print('Undoing...')
        self.__last_cmd.unexecute()

class Main(object):
    """
    $ python src/patterns/command.py

    Clicking slot 1 on button...
    Kitchen light is on
    Clicking slot 1 off button...
    Kitchen light  is off
    Clicking slot 0 on button...
    Living Room light is on
    Clicking slot 0 off button...
    Living Room light  is off
    Clicking slot 2 on button...
    Living Room light is on
    Kitchen light is on
    Clicking slot 2 off button...
    Living Room light  is off
    Kitchen light  is off
    Undoing...
    Living Room light is on
    Kitchen light is on

    """

    def main(self):
        light1 = Light('Living Room')
        light2 = Light('Kitchen')
        light1oncmd = LightOnCommand(light1)
        light1offcmd = LightOffCommand(light1)
        light2oncmd = LightOnCommand(light2)
        light2offcmd = LightOffCommand(light2)
        macro_on_cmd = MacroCommand([light1oncmd, light2oncmd])
        macro_off_cmd = MacroCommand([light1offcmd, light2offcmd])

        remote_control = RemoteControl(3)
        remote_control.set_command(0, light1oncmd, light1offcmd)
        remote_control.set_command(1, light2oncmd, light2offcmd)
        remote_control.set_command(2, macro_on_cmd, macro_off_cmd)

        remote_control.click_on(1)
        remote_control.click_off(1)
        remote_control.click_on(0)
        remote_control.click_off(0)
        remote_control.click_on(2)
        remote_control.click_off(2)
        remote_control.undo()

if __name__ == '__main__':
    Main().main()
