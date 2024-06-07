import win32api
import win32gui
import win32ui
import numpy as np
from typing import Union
import ctypes
from Rectangle import Rect


def isValidHandle(window_handle: int) -> bool:
    """Checks if the handle is valid

    Args:
        window_handle (int): Handle for the window
    """
    if not isinstance(window_handle, int):
        raise TypeError("Window handle must be an integer")
    return win32gui.IsWindow(window_handle)

def getWindowHandle(window_title: str) -> int:
    """Gets the windows window handler [probably a pointer?]

    Args:
        window_title (str): The title of the window

    Returns:
        WindowHanlder: The windows window handler [probably a pointer?]
    """
    if not isinstance(window_title, str):
        raise TypeError("The window_title must be a str")
    
    # Returns a windows window handler object
    hwnd = win32gui.FindWindow(None, window_title)

    if hwnd is None:
        raise ValueError("The window does not exists")
    
    return hwnd

def isWindowOpen(window_title: str) -> bool:
    """Checks if there is a window with the provided title.

    Args:
        window_title (string): Title of the window to be checked

    Returns:
        Bool: Returns true, if there is a window with the provided title.
    """
    if not isinstance(window_title, str):
        raise TypeError("The window_title must be a str")

    hwnd = win32gui.FindWindow(None, window_title)
    return hwnd is not None

def getWindowRect(window: Union[str,int]) -> list:
    if not isinstance(window, (str,int)):
        raise TypeError("Window must be the title (a string) or the handler (an integer)")

    if isinstance(window,int):
        if not isValidHandle(window):
            raise ValueError("Invalid window handle")
        hwnd = window
    
    if isinstance(window, str):
        hwnd = getWindowHandle(window)

    rect = win32gui.GetWindowRect(hwnd)
    rect = Rect(rect)
    return rect


if __name__ == "__main__":
    getWindowRect("GitHub Desktop")
    print(getWindowHandle("GitHub Desktop"))