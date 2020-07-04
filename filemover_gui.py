#
# File Mover GUI
# GUI implementation for File Mover using PyQt5
#
# Copyright (c) KvinTanaka. (MIT License)
# https://www.kvintanaka.com
#

import sys
import os
from interface import implements
from filemover import FileMover, FileMoverObserver
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
from PyQt5 import QtCore


class FileMoverGUI(QMainWindow):
    """GUI Implementation for File Mover
    Author: KvinTanaka"""

    class FileMoverObserverImplementation(implements(FileMoverObserver)):
        """Modified observer implementation to make message available for polling
        Author: KvinTanaka"""

        def __init__(self):
            self.message = ""

        def update(self, message) -> None:
            """Receive update from FileMover (Observer Implementation)
            Author: KvinTanaka"""
            self.message = message

    def __init__(self, filemover):
        super(FileMoverGUI, self).__init__()
        loadUi('filemover_gui.ui', self)

        self.filemover = filemover
        self.observer = self.FileMoverObserverImplementation()
        self.filemover.attach(self.observer)

        self.choose_source_button.clicked.connect(self.choose_source_button_clicked)
        self.choose_destination_button.clicked.connect(self.choose_destination_button_clicked)
        self.mover_button.clicked.connect(self.mover_button_clicked)

        self.mover_button.setEnabled(self.directory_status())

    @QtCore.pyqtSlot(name="mover_button_clicked")
    def mover_button_clicked(self):
        """ Event handler for mover button
        Note: QtCore.pyqtSlot() is needed to prevent auto-slot assignment
        Which can lead to undefined behaviour (Several click at once)
        Author: KvinTanaka"""

        if self.filemover.running:
            self.filemover.stop()
            self.mover_button.setText("Start Moving")
            self.source_directory_text.setEnabled(True)
            self.destination_directory_text.setEnabled(True)
            self.choose_source_button.setEnabled(True)
            self.choose_destination_button.setEnabled(True)
        else:
            self.filemover.start()
            self.mover_button.setText("Stop Moving")
            self.source_directory_text.setEnabled(False)
            self.destination_directory_text.setEnabled(False)
            self.choose_source_button.setEnabled(False)
            self.choose_destination_button.setEnabled(False)
        self.information_label.setText(self.observer.message)

    @QtCore.pyqtSlot(name="choose_source_button_clicked")
    def choose_source_button_clicked(self):
        """Event Handler for source button
        Author: KvinTanaka"""

        source_path = self.choose_directory()

        self.source_directory_text.setText(source_path)
        self.filemover.source_path = os.path.normpath(source_path)

        self.mover_button.setEnabled(self.directory_status())

    @QtCore.pyqtSlot(name="choose_destination_button_clicked")
    def choose_destination_button_clicked(self):
        """Event Handler for destination button
        Author: KvinTanaka"""

        destination_path = self.choose_directory()

        self.destination_directory_text.setText(destination_path)
        self.filemover.destination_path = os.path.normpath(destination_path)

        self.mover_button.setEnabled(self.directory_status())

    @staticmethod
    def choose_directory() -> str:
        """Choose directory by using QFileDialog
        Author: KvinTanaka"""

        directory_dialog = QFileDialog()
        directory_dialog.setFileMode(QFileDialog.Directory)
        return directory_dialog.getExistingDirectory()

    def directory_status(self) -> bool:
        """Check whether source and destination path is filled in the form
        Author: KvinTanaka"""
        return self.filemover.source_path is not None and self.filemover.destination_path is not None


def main():
    """Start point"""

    app = QApplication(sys.argv)
    window = FileMoverGUI(FileMover())

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
