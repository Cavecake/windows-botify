from . import window_api
from .window_api import __get_handle_from_function_params
import win32con
import win32api

class MouseButton:
    LEFT = win32con.MK_LBUTTON
    RIGHT = win32con.MK_RBUTTON
    MIDDLE = win32con.MK_MBUTTON

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

def getMousePos():
    """Gets the position of the cursor

    Returns:
        x, y: Coordinates
    """
    return win32api.GetCursorPos()

def ButtonDown(window,mouse_button, x = None, y = None, isRelativeToWindow = False, activationLevel = 1):
    """Presses the mouse button

    Args:
        window (str, int): The title or handle for the window
        mouse_button (int): The windows button (Use MouseButton from windows_botify.mouse)
        x (int, optional): The x position of the position the mouse should click. Defaults to None.
        y (int, optional): The y position of the position the mouse should click. Defaults to None.
        isRelativeToWindow (bool, optional): Are the coordinates relative to the screen or the window. Defaults to False.
        activationLevel (int, optional): The level of activation for the window, the input is send to (activation allows the process to process inputs)
    """
    hwnd = window_api.__get_handle_from_function_params(window) # Inbuilt error correction
    old_hwnd = window_api.enableInputFocus(hwnd,activationLevel)

    if x is None or y is None:
        x, y = getMousePos()
    elif isRelativeToWindow:
        x, y = window_api.cvtWindowToScreenCoordinates(window, x, y)
    elif not (isinstance(x, int) and isinstance(y, int)):
        raise TypeError("Coordinates must be an integer")
    
    if mouse_button not in BUTTON_DOWN_MAP.keys():
        raise ValueError("Invalid mouse button. Use the mouse.MOUSE_BUTTON.BUTTON_NAME values.")

    lParam = win32api.MAKELONG(x, y)
    wParam = mouse_button

    win32api.PostMessage(hwnd,[BUTTON_DOWN_MAP[mouse_button]], wParam, lParam)

    try:
        window_api.enableInputFocus(old_hwnd,activationLevel)
    except Exception:
        pass

def ButtonUp(window,mouse_button, activationLevel = 1):
    """Releases the mouse button

    Args:
        window (str, int): The title or handle for the window
        mouse_button (int): The windows button (Use MouseButton from windows_botify.mouse)
        activationLevel (int, optional): The level of activation for the window, the input is send to (activation allows the process to process inputs)
    """
    hwnd = window_api.__get_handle_from_function_params(window) # Inbuilt error correction
    old_hwnd = window_api.enableInputFocus(hwnd,activationLevel)
    
    x, y = getMousePos()
    
    if mouse_button not in BUTTON_UP_MAP.keys():
        raise ValueError("Invalid mouse button. Use the mouse.MOUSE_BUTTON.BUTTON_NAME values.")
    
    lParam = win32api.MAKELONG(x, y)
    wParam = mouse_button

    win32api.PostMessage(hwnd,[BUTTON_UP_MAP[mouse_button]], wParam, lParam)

    try:
        window_api.enableInputFocus(old_hwnd,activationLevel)
    except Exception:
        pass

def Scroll(window,delta, activationLevel = 1):
    """Scrolls with the mouse

    Args:
        window (str, int): The title or handle for the window
        delta (_type_): The movement of the mouse positive = Scroll up
        activationLevel (int, optional): The level of activation for the window, the input is send to (activation allows the process to process inputs)
    """
    if not isinstance(delta, int):
        raise TypeError("Delta (scroll amount) must be an integer")
    

    hwnd = __get_handle_from_function_params(window)
    old_hwnd = window_api.enableInputFocus(hwnd,activationLevel)

    x, y = getMousePos()  # Get the current cursor position

    lParam = win32api.MAKELONG(x, y)
    wParam = (delta << 16) | (0 & 0xFFFF)

    win32api.PostMessage(hwnd, win32con.WM_MOUSEWHEEL, wParam, lParam)
    try:
        window_api.enableInputFocus(old_hwnd,activationLevel)
    except Exception:
        pass