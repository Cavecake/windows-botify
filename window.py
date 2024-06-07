import win32api
import win32gui
import win32con
import win32ui
import numpy as np
from typing import Union
import ctypes
from Rectangle import Rect

def __get_handle_from_function_params(window):
    if not isinstance(window, (str,int)):
        raise TypeError("Window must be the title (a string) or the handler (an integer)")

    if isinstance(window,int):
        if not isValidHandle(window):
            raise ValueError("Invalid window handle")
        hwnd = window
    
    if isinstance(window, str):
        hwnd = getWindowHandle(window)

    return hwnd

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
    hwnd = __get_handle_from_function_params(window)
    rect = win32gui.GetWindowRect(hwnd)
    rect = Rect(rect)
    return rect

def moveToForeground(window: Union[str,int]) -> None:
    """Moves the window with the given handle to the foreground"""
    hwnd = __get_handle_from_function_params(window)
    win32gui.SetForegroundWindow(hwnd)

def minimizeWindow(window: Union[str,int]) -> None:
    """Moves the window with the given handle to the background"""
    hwnd = __get_handle_from_function_params(window)
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

def getWindowScreenshot(window, Windows_PrintWindow_Flag = 3):
    hwnd = __get_handle_from_function_params(window)
    # Graphical interface (windows types)
    hwndDC = win32gui.GetWindowDC(hwnd)
    # Connection to hwndDC (windows types)
    hdc = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = hdc.CreateCompatibleDC()

    # Requires the widht and hight, which is read here
    rect: Rect = getWindowRect(hwnd)
    _, w, h = rect.getDimensions()

    # Create a bitmap compatible with the device context
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(hdc, w, h)

    saveDC.SelectObject(bmp)

    # getting results
    result = ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), Windows_PrintWindow_Flag)
    
    # Retrieve data from bitmap
    bmp_info = bmp.GetInfo()
    bmp_str = bmp.GetBitmapBits(True)

    # Convert the bitmap bits to a numpy array
    arr = np.frombuffer(bmp_str, dtype=np.uint8)
    arr.shape = (bmp_info['bmHeight'], bmp_info['bmWidth'], 4)  # Assuming 32-bit RGBA

    # Free Handles
    win32gui.DeleteObject(bmp.GetHandle())
    saveDC.DeleteDC()
    hdc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    return arr
if __name__ == "__main__":
    moveToForeground("GitHub Desktop")
    print(getWindowHandle("GitHub Desktop"))