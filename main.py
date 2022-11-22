"""Main Phonebook script
"""

from database import Database
from entry import Entry
# from inputLib import *


if __name__ == "__main__":
    def main():
        """main function of this programm
        """
        data_base = Database()
        print(data_base.folder)
        print(data_base.files)
        entry = Entry()
        print(entry.file)
        entry.print()
        if entry.save():
            print(entry.file)
            entry1, oks = Entry.load(entry.file)
            if oks:
                print(entry1.file)
                print("ok")
                entry1.print()

    main()
