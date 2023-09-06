"""
- The model uses Observer to keep the views and controllers updated on the latest state changes.
- The view and the controller, implements the Strategy Pattern. The controller is the strategy of the view.
- The view itself uses the Composite Pattern to manage the windows, buttons, and other components of the display.
- The view is concerned with the visual aspects of the application,
  and delegates to the controller any decisions about the interface behaviors.

Below code is incomplete.
"""
from abc import ABC, abstractmethod
import time

class AbsBeatModelInterface(ABC):
    """
    The model is responsible for maintaining all the data, state, and any application logic.

    Uses the Observer Pattern.
    """

    @abstractmethod
    def initialize(self):
        """
        This gets called after BeatModel is instantiated.
        """

    @abstractmethod
    def on(self):
        """
        Turn the beat generator on.
        """

    @abstractmethod
    def off(self):
        """
        Turn the beat generator off.
        """

    @abstractmethod
    def set_bpm(self, bpm):
        """
        Set the beats per minute. After it is called, the beat frequency changes immediately.
        """

    @abstractmethod
    def get_bpm(self):
        pass

    def register_beat_observer(self, beat_observer):
        """
        Observers that want to be notified on every beat.
        """

    def remove_beat_observer(self, beat_observer):
        pass

    def register_bpm_observer(self, bpm_observer):
        """
        Observers that want to be notified when the bpm changes.
        """

    def remove_bpm_observer(self, bpm_observer):
        pass

class BeatModel(AbsBeatModelInterface):

    def __init__(self):
        self.__beat_observers = []
        self.__bpm_observers = []
        self.__bpm = 90
        self.__stop = False

    def initialize(self):
        """
        This method does setup for the beat track.
        """
        print('Clip opened')

    def on(self):
        self.__bpm = 90
        self.notify_bpm_observers()
        self.__stop = False

    def off(self):
        self.__stop_beat()
        self.__stop = True

    def run(self):
        while not self.__stop:
            self.__play_beat()
            self.notify_beat_observers()
            time.sleep(6e4 / self.get_bpm())

    def __stop_beat(self):
        print('Set clip to position 0')
        print('Stop clip')

    def __play_beat(self):
        print('Set clip to position 0')
        print('Play clip')

    def set_bpm(self, bpm):
        self.__bpm = bpm
        self.notify_bpm_observer()

    def get_bpm(self):
        return self.__bpm

    def register_beat_observer(self, beat_observer):
        self.__beat_observers.append(beat_observer)

    def register_bpm_observer(self, bpm_observer):
        self.__bpm_observers.append(bpm_observer)

    def notify_beat_observers(self):
        for observer in self.__beat_observers:
            observer.update_beat()

    def notify_bpm_observers(self):
        for observer in self.__bpm_observers:
            observer.update_bpm()

class AbsBeatObserver(ABC):

    @abstractmethod
    def update_beat(self):
        pass

class AbsBpmObserver(ABC):

    @abstractmethod
    def update_bpm(self):
        pass

class DJView(AbsBeatObserver, AbsBpmObserver):

    def __init__(self, controller, beat_model):
        self.__controller = controller
        self.__beat_model = beat_model
        self.__beat_model.register_beat_observer(self)
        self.__beat_model.register_bpm_observer(self)

    def create_view(self):
        pass

    def create_controls(self):
        pass

    def enable_start_menu_item(self):
        pass

    def disable_start_menu_item(self):
        pass

    def enable_stop_menu_item(self):
        pass

    def disable_stop_menu_item(self):
        pass

class AbsController(ABC):

    def start(self):
        pass

    def stop(self):
        pass

    def increase_bpm(self):
        pass

    def decrease_bpm(self):
        pass

    def set_bpm(self, bpm):
        pass

class BeatController(AbsController):

    def __init__(self, beat_model):
        self.__beat_model = beat_model
        self.__view = DJView(self, self.__beat_model)
        self.__view.create_view()
        self.__view.create_controls()
        self.__view.disable_stop_menu_item()
        self.__view.enable_start_menu_item()
        self.__beat_model.initialize()

    def start(self):
        self.__beat_model.on()
        self.__view.disable_start_menu_item()
        self.__view.enable_stop_menu_item()

    def stop(self):
        self.__beat_model.off()
        self.__view.disable_stop_menu_item()
        self.__view.enable_start_menu_item()

    def increase_bpm(self):
        self.__beat_model.set_bpm(self.__beat_model.get_bpm() + 1)

    def decrease_bpm(self):
        self.__beat_model.set_bpm(self.__beat_model.get_bpm() - 1)

    def set_bpm(self, bpm):
        self.__beat_model.set_bpm(bpm)




