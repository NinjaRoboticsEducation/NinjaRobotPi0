import sys
import select
import termios
import tty

class NonBlockingKeyboard:
    """A class to handle non-blocking keyboard input."""
    def __enter__(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def kbhit(self):
        """Check if a key has been pressed."""
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

    def getch(self):
        """Get the pressed character."""
        return sys.stdin.read(1)
