import sys

from PyQt6.QtWidgets import QApplication

from pyqt_histogram.gui.mainwin.MainWindow import MainWindow

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    print(win.histogram.size())
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
