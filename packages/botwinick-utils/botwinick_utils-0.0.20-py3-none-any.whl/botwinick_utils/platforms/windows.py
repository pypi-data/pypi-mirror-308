# Some useful references for Windows app stuff

import ctypes
import sys


def allocate_console():
    """
    Allocate a console using Windows APIs (useful to pop up a console for a GUI application without a console attached)

    Note that if there is already a console attached to the process, then this will not create another one.
    """
    ctypes.windll.kernel32.AllocConsole()


def free_console():
    """
    Free console using Windows APIs.
    """
    ctypes.windll.kernel32.FreeConsole()


def open_console_stream():
    """
    Open a new output stream to allocated console.
    """
    return open("CONOUT$", "w")


def hide_console_window():
    """
    Hide console window allocated to this process.
    """
    wnd = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.ShowWindow(wnd, 0)  # SW_HIDE


def show_console_window():
    """
    Show console window allocated to this process.
    """
    wnd = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.ShowWindow(wnd, 5)  # SW_SHOW


def redirect_std_streams_to_console():
    """
    Assign new output streams to allocated console to sys.stdout and sys.stderr
    """
    sys.stdout = open_console_stream()
    sys.stderr = open_console_stream()
