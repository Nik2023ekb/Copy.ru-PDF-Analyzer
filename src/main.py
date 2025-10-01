"""GUI entrypoint."""
import sys
from PySide6.QtWidgets import QApplication
from .gui import MainWindow

def main(argv=None):
    app = QApplication(argv or [])
    w = MainWindow()
    w.show()
    return app.exec()

if __name__ == "__main__":
    raise SystemExit(main())
