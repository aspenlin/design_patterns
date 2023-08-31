"""
Composite Pattern
- Whenever you design "container" objects that collect and organize "content" object,
  you will simplify many operations for the caller if you give container objects and content objects a shared set of methods
  and thereby support as many operations as possible without the caller having to care whether they have been
  passed an individual content object or an entire container.
- This is a general idea not only applied to object based programming (e.g. Linux treats everything as a file)
- The art of using the Composite Pattern is determining where to break the symmetry.
  e.g. the UNIX filesystem provides completely different commands `touch` for creating a new file and `mkdir` for
  creating a new directory

Refer to: https://python-patterns.guide/gang-of-four/composite/
"""
from tkinter import Tk, Frame, Button

class Widget(object):

    def children(self):
        """
        For containers, it returns their list of child widgets. For other widgets, it simply returns an empty list.
        """
        return []

class SimpleFrame(Widget):
    def __init__(self, child_widgets):
        self.child_widgets = child_widgets

    def children(self):
        return self.child_widgets

class SimpleButton(Widget):
    """
    Some people may argue it does not make sense for Button to implement a `children()` method.
    But this same interface offers symmetry between Button and Frame and gives clients simplicity.
    """
    def __init__(self, text):
        self.text = text

def print_tree(widget, indent=0):
    """Print a hierarchy of Tk widgets in the terminal."""
    print('{:<{}} * {!r}'.format('', indent * 4, widget))
    for child in widget.winfo_children(): # Client no need to check whether widget has winfo_children method
        print_tree(child, indent + 1)

if __name__ == '__main__':
    """
    Print widget tree gives:
     * <tkinter.Frame object .!frame>
         * <tkinter.Button object .!frame.!button>
         * <tkinter.Button object .!frame.!button2>
    """
    root = Tk()
    f = Frame(master=root)
    f.pack()

    tree_button = Button(f)
    tree_button['text'] = 'Print widget tree'
    tree_button['command'] = lambda: print_tree(f)
    tree_button.pack({'side': 'left'})

    quit_button = Button(f)
    quit_button['text'] = 'Quit Tk application'
    quit_button['command'] = f.quit
    quit_button.pack({'side': 'left'})

    f.mainloop()
    root.destroy()

