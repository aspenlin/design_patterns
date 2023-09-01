"""
Proxy Pattern
- The Proxy Pattern provides a surrogate or placeholder for another object to CONTROL ACCESS to it.
- Use the Proxy Pattern to create a representative object that controls access to another object,
  which may be remote, expensive to create, or in need of securing.

- Remote Proxy (manages iteration between a client and a remote object)
- Virtual Proxy (controls access to an object that is expensive to instantiate)
- Protection Proxy (controls assess to the methods of an object based on the caller)
- Many other variants
"""
from abc import ABC, abstractmethod

class AbsIcon(ABC):
    """
    Interface for both the real subject and the proxy.
    """

    @abstractmethod
    def get_icon_width(self):
        pass

    @abstractmethod
    def get_icon_height(self):
        pass

    @abstractmethod
    def paint_icon(self):
        pass

class ImageIcon(AbsIcon):
    """
    ImageIcon is the real subject.
    """

    def __init__(self, image_url):
        # load image from the url
        pass

    def get_icon_width(self):
        pass

    def get_icon_height(self):
        pass

    def paint_icon(self):
        pass



class ImageProxy(AbsIcon):
    """
    ImageProxy controls access to ImageIcon.
    """

    def __init__(self, image_url):
        self.__image_url = image_url
        self.__image_icon = None

    def get_icon_width(self):
        if self.__image_icon is not None:
            return self.__image_icon.get_icon_width()
        return 800

    def get_icon_height(self):
        if self.__image_icon is not None:
            return self.__image_icon.get_icon_height()
        return 600

    def paint_icon(self):
        if self.__image_icon is not None:
            self.__image_icon.paint_icon()
        else:
            print('Loading album cover, please wait...')
            try:
                self.__image_icon = ImageIcon(self.__image_url)
                self.__image_icon.paint_icon()
            except BaseException as e:
                print(f'Unable to instantiate ImageIcon due to {e}')

if __name__ == '__main__':
    image_url = 'https://abc.img'
    image_proxy = ImageProxy(image_url)
    image_proxy.paint_icon()


