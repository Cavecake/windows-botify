from . import window_api
from .window_api import __get_handle_from_function_params as __get_handle_from_function_params
from .rectangle import Rect
import win32con
import win32api
from typing import Union
from warnings import warn

class MouseButton:
    LEFT = win32con.MK_LBUTTON
    RIGHT = win32con.MK_RBUTTON
    MIDDLE = win32con.MK_MBUTTON

class Modifiers:
    # All Modifieres a represented with a single bit
    SHIFT = win32con.VK_SHIFT
    CONTROL = win32con.VK_CONTROL
    ALT = win32con.VK_MENU

BUTTON_DOWN_MAP = {
    MouseButton.LEFT: win32con.WM_LBUTTONDOWN,
    MouseButton.RIGHT: win32con.WM_RBUTTONDOWN,
    MouseButton.MIDDLE: win32con.WM_MBUTTONDOWN,
}

BUTTON_UP_MAP = {
    MouseButton.LEFT: win32con.WM_LBUTTONUP,
    MouseButton.RIGHT: win32con.WM_RBUTTONUP,
    MouseButton.MIDDLE: win32con.WM_MBUTTONUP,
}

BUTTON_MODIFIERS = {
    MouseButton.LEFT: win32con.MK_LBUTTON,
    MouseButton.RIGHT: win32con.MK_RBUTTON,
    MouseButton.MIDDLE: win32con.MK_MBUTTON,
}

def __createWparam(modifiers, buttons = []):
    """Creates the Wparam for the SendMessage function

    Args:
        modifiers:  A set of modifier keys, e.g., {win32con.VK_SHIFT, win32con.VK_CONTROL}.

    Returns:
        wParam value.
    """
    wParam = 0
    
    # Bitwise OR the modifier key values to construct wParam
    for modifier in modifiers:
        wParam |= modifier

    # Bitwise OR the mouse button values to construct wParam
    for button in buttons:
        wParam |= button
    
    return wParam


def getMousePos():
    """Gets the position of the cursor

    Returns:
        x, y: Coordinates
    """
    return win32api.GetCursorPos()

def ButtonDown(window,mouse_button, x = None, y = None, isRelativeToWindow = False, modifiers = []):
    """Presses the mouse button

    Args:
        window (str, int): The title or handle for the window
        mouse_button (int): The windows button (Use MouseButton from windows_botify.mouse)
        x (int, optional): The x position of the position the mouse should click. Defaults to None.
        y (int, optional): The y position of the position the mouse should click. Defaults to None.
        isRelativeToWindow (bool, optional): Are the coordinates relative to the screen or the window. Defaults to False.
        modifiers (list, optional): Modifieres like Ctrl, Shift or Alt. (Use Modifiers from windows_botify.mouse) Defaults to [].
    """
    hwnd = window_api.__get_handle_from_function_params(window) # Inbuilt error correction
    
    if x is None or y is None:
        x, y = getMousePos()
    elif isRelativeToWindow:
        x, y = window_api.cvtWindowToScreenCoordinates(window, x, y)
    elif not (isinstance(x, int) and isinstance(y, int)):
        raise TypeError("Coordinates must be an integer")
    
    if mouse_button not in BUTTON_DOWN_MAP.keys():
        raise ValueError("Invalid mouse button. Use the mouse.MOUSE_BUTTON.BUTTON_NAME values.")
    
    for modifier in modifiers:
        if modifier not in {Modifiers.SHIFT, Modifiers.CONTROL, Modifiers.ALT}:
            raise ValueError("Invalid modifier key. Use Modifiers.SHIFT, Modifiers.CONTROL, or Modifiers.ALT.")

    lParam = win32api.MAKELONG(x, y)
    wParam = __createWparam(modifiers,mouse_button)

    win32api.SendMessage(hwnd,BUTTON_DOWN_MAP[mouse_button], wParam, lParam)

def ButtonUp(window,mouse_button):
    """Releases the mouse button

    Args:
        window (str, int): The title or handle for the window
        mouse_button (int): The windows button (Use MouseButton from windows_botify.mouse)
    """
    hwnd = window_api.__get_handle_from_function_params(window) # Inbuilt error correction
    
    x, y = getMousePos()
    
    if mouse_button not in BUTTON_UP_MAP.keys():
        raise ValueError("Invalid mouse button. Use the mouse.MOUSE_BUTTON.BUTTON_NAME values.")
    
    lParam = win32api.MAKELONG(x, y)
    wParam = mouse_button

    win32api.SendMessage(hwnd,BUTTON_UP_MAP[mouse_button], wParam, lParam)

def Scroll(window,delta, modifiers = []):
    """Scrolls with the mouse

    Args:
        window (str, int): The title or handle for the window
        delta (_type_): The movement of the mouse positive = Scroll up
        modifiers (list, optional): Modifieres like Ctrl, Shift or Alt. (Use Modifiers from windows_botify.mouse) Defaults to [].
    """
    if not isinstance(delta, int):
        raise TypeError("Delta (scroll amount) must be an integer")
    
    hwnd = __get_handle_from_function_params(window)
    x, y = getMousePos()  # Get the current cursor position

    lParam = win32api.MAKELONG(x, y)

    modifiers = __createWparam(modifiers)
    wParam = (delta << 16) | (modifiers & 0xFFFF)

    win32api.SendMessage(hwnd, win32con.WM_MOUSEWHEEL, wParam, lParam)