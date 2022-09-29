import sys
import os
import logging
import typer

from PyQt6.QtWidgets import QApplication

from pyqt_histogram.gui.mainwin.MainWindow import MainWindow

app = typer.Typer()


@app.command()
def default(with_logging: bool = False, log_level: str = "debug", log_file: str = "histo.log", log_append: bool = False):

    if with_logging:
        if not log_append:
            if os.path.isfile(log_file):
                os.remove(log_file)
        logging.basicConfig(filename=log_file, encoding="utf-8", level=logging.getLevelName(log_level.upper()))

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()

    logging.debug(win.histogram.size())

    sys.exit(app.exec())


def main():

    app()


if __name__ == "__main__":

    main()
