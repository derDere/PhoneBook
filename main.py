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
        entry.save()

    main()
