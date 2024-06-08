import win32api
import win32gui
import win32con
import win32ui
import numpy as np
from typing import Union
import ctypes
from .rectangle import Rect

def __get_handle_from_function_params(window):
    """Internal function. Do not use.
    Converts a window str or handle to a hande. Checks validity

    Args:
        window (str, int): Window handle or window name

    Returns:
        int: The window handle
    """
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

    if hwnd is None or hwnd == 0:
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
    """Gets the bounding Rect of the window

    Args:
        window (Union[str,int]): The window handle or window title

    Returns:
        Rect: The bounding Rect of the screen 
    """
    hwnd = __get_handle_from_function_params(window)
    rect = win32gui.GetWindowRect(hwnd)
    rect = Rect(rect)
    return rect

def moveToForeground(window: Union[str,int]) -> None:
    """Moves the window to the foreground

    Args:
        window (Union[str,int]): The window handle or window title
    """
    hwnd = __get_handle_from_function_params(window)
    win32gui.SetForegroundWindow(hwnd)

def minimizeWindow(window: Union[str,int]) -> None:
    """Moves the window to the background
    
    Args:
        window (Union[str,int]): The window handle or window title
    """
    hwnd = __get_handle_from_function_params(window)
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

def move_window(window: Union[str,int], x, y):
    """Move the window to the specified position
    
    Args:
        window (Union[str,int]): The window handle or window title
    """
    hwnd = __get_handle_from_function_params(window)
    win32gui.SetWindowPos(hwnd, 0, x, y, 0, 0, 0x0001 | 0x0002)  # SWP_NOSIZE | SWP_NOZORDER

def scale_window(window: Union[str,int], width, height):
    """Scale the window to the specified size
    
    Args:
        window (Union[str,int]): The window handle or window title
    """
    hwnd = __get_handle_from_function_params(window)
    win32gui.SetWindowPos(hwnd, 0, 0, 0, width, height, 0x0001 | 0x0002)  # SWP_NOMOVE | SWP_NOZORDER

def getWindowScreenshot(window: Union[str,int], Windows_PrintWindow_Flag = 3):
    """Takes a screenshot of the window

    Args:
        window (str, int): The windows window handle or the name of the window
        Windows_PrintWindow_Flag (int, optional): Some flag, windows requires. In case the function does not work try to change the value. Defaults to 3.

    Returns:
        ndarray: A numpy array of the image.
    """
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

def getPixelColor(window, x, y, isRelativeToWindow = False, Windows_PrintWindow_Flag = 3):
    """Gets 

    Args:
        window (str, int): The handle or title for the window
        x (int): The x position of the pixel
        y (int): The y position of the pixel
        isRelativeToWindow (bool, optional): Are the positions relative to the upper left screen corner or the upper left window corner. Defaults to False.
        Windows_PrintWindow_Flag (int, optional): Some flag, windows requires. In case the function does not work try to change the value. Defaults to 3.

    Returns:
        tuple: The RGBA Color of the pixel
    """
    img = getWindowScreenshot(window,Windows_PrintWindow_Flag)
    if isRelativeToWindow:
        x, y = cvtScreenToWindowCoordinates(window, x, y)

    if 0 <= y <= len(img) and 0 <= x < len(img[0]):
        raise IndexError("Your points must be inside the window. (0,0) is the window corner")
    return img[y][x]

def cvtWindowToScreenCoordinates(window: Union[int, str, Rect], x: int, y: int):
    """Converts the coordinates relativ to the window corner to coordinates relative to the screen coordinates

    Args:
        window (Union[int, str, Rect]): Either the bounding Rect of the window, or the handle/title of the window
        x (int): x coordinate
        y (int): y coordinate
    """
    if not isinstance(x, int) or not isinstance(y, int) :
        raise TypeError("Coordinates must be integers")
    
    if isinstance(window,(str,int)):
        window_rect = getWindowRect(window)
    elif isinstance(window, Rect):
        window_rect = window
    else:
        raise TypeError("Window must be either the bounding Rect of the window, or the handle/title of the window")

    upper_left, _ = window_rect.getCornerPoints()
    x2, y2 = upper_left

    return x2 + x, y2 + y
def cvtScreenToWindowCoordinates(window: Union[int, str, Rect], x: int, y: int):
    """Converts the coordinates relativ to the screen corner to coordinates relative to the window coordinates

    Args:
        window (Union[int, str, Rect]): Either the bounding Rect of the window, or the handle/title of the window
        x (int): x coordinate
        y (int): y coordinate
    """
    if not isinstance(x, int) or not isinstance(y, int) :
        raise TypeError("Coordinates must be integers")
    
    if isinstance(window,(str,int)):
        window_rect = getWindowRect(window)
    elif isinstance(window, Rect):
        window_rect = window
    else:
        raise TypeError("Window must be either the bounding Rect of the window, or the handle/title of the window")

    upper_left, _ = window_rect.getCornerPoints()
    x2, y2 = upper_left

    return x - x2, y - y2

if __name__ == "__main__":
    moveToForeground("GitHub Desktop")
    print(getWindowHandle("GitHub Desktop"))