import ctypes
import sys


def lock_workstation():
    if sys.platform == "win32":
        ctypes.windll.user32.LockWorkStation()


def unlock_workstation():
    """Windows intentionally does not expose a supported programmatic unlock API."""
    return True
