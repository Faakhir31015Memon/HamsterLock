import sys


class WindowManager:
    def __init__(self, pygame):
        self.pygame = pygame

    def create(self, size):
        flags = self.pygame.FULLSCREEN | self.pygame.NOFRAME | self.pygame.HWSURFACE | self.pygame.DOUBLEBUF
        return self.pygame.display.set_mode(size, flags)

    def keep_on_top(self):
        if sys.platform != "win32":
            return
        try:
            import ctypes
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            HWND_TOPMOST, SWP_NOMOVE, SWP_NOSIZE = -1, 0x0002, 0x0001
            ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
        except Exception:
            pass
