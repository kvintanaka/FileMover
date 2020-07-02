#
# File Mover
# Move file continuously from a low-space source to a destination for storage
#
# Copyright (c) KvinTanaka. (MIT License)
# https://www.kvintanaka.com
#


from interface import Interface, implements
from threading import Thread
import os
import sys
import shutil


# --- File Mover - Misc ---


class FileMoverObserver(Interface):

    def update(self, message) -> None:
        """Receive update from FileMover
        Author: KvinTanaka"""
        pass


# --- File Mover - Main ---


class FileMover:

    def __init__(self, source_path=None, destination_path=None):
        """Initialise file mover with source and destination path
        Initially will not running
        Author: KvinTanaka"""

        self.running = False
        if source_path is not None:
            source_path = os.path.normpath(source_path)
            self.check_path(source_path)
        self.source_path = source_path
        if destination_path is not None:
            destination_path = os.path.normpath(destination_path)
            self.check_path(destination_path)
        self.destination_path = destination_path
        self.observers = []

    def attach(self, observer: FileMoverObserver) -> None:
        """Attach an observer to the subject.
        Author: KvinTanaka"""

        self.observers.append(observer)

    def detach(self, observer: FileMoverObserver) -> None:
        """Detach an observer from the subject.
        Author: KvinTanaka"""

        self.observers.remove(observer)

    def notify(self, message: str) -> None:
        """Notify all observers about an event.
        Author: KvinTanaka"""

        [observer.update(message) for observer in self.observers]

    def start(self):
        """Start moving file from source to destination
        Author: KvinTanaka"""

        self.running = True
        self.notify("File moving started")

        self.do_file_move()

    def stop(self):
        """Stop moving file from source to destination
        Author: KvinTanaka"""

        self.running = False
        self.notify("File moving stopped")

    @staticmethod
    def found_new_file(path):
        """Check for a new available file
        Author: KvinTanaka"""

        return len(os.listdir(path)) > 0

    @staticmethod
    def check_path(path):
        """Check for a new available file
        Author: KvinTanaka"""

        if not os.path.exists(path):
            raise Exception(str(path) + " is not exists")

    def do_file_move(self):
        """Move file detected in source directory to destination directory
        Author: KvinTanaka"""

        counter = 0
        while self.running:
            if self.found_new_file(self.source_path):
                for filename in os.listdir(self.source_path):
                    source_file = os.path.join(self.source_path, filename)
                    if os.path.isfile(source_file):
                        destination_file = os.path.join(self.destination_path, filename)

                        shutil.copy(source_file, destination_file)
                        os.remove(source_file)

                        counter += 1
                        self.notify(str(counter) + " File Moved")


class FileMoverObserverImplementation(implements(FileMoverObserver)):
    """Observer Implementation for CLI UI
    Author: KvinTanaka"""
    def update(self, message):
        print(f'{message}\r', end="")


def main():
    """Start point"""

    source_path = os.path.normpath(str(sys.argv[1]))
    destination_path = os.path.normpath(str(sys.argv[2]))

    if os.path.exists(source_path) and os.path.exists(destination_path):
        filemover = FileMover(source_path, destination_path)
        filemover.attach(FileMoverObserverImplementation())

        filemover.start()


if __name__ == "__main__":
    main()
