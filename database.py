"""Contains all functions and classes to store and manage all data from your phone book.
"""

import os
import random as rnd
import datetime
from os.path import isfile, exists, join

import path_config
from entry import Entry
from input_lib import input_bool, InputAbortException, InputExitException


class Database:
    """This class represents one database manager object used to manage your phonebook
    """

    def __init__(self) -> None:
        self.contacts = []
        self.folder = path_config.get_folder_path()
        if not exists(self.folder):
            os.makedirs(self.folder)
            self.files = []
            print("No folder found. New one was created!")
        else:
            self.files = [
                f for f in os.listdir(self.folder)
                if (
                    isfile(join(self.folder, f)) and
                    (f.lower()[-len(path_config.FILE_EXTENSINON):] == path_config.FILE_EXTENSINON)
                )
            ]
        print_status = len(self.files) > 200
        count = 0
        failed = 0
        max_out_len = 0
        for file in self.files:
            entry, success = Entry.load(join(self.folder, file))
            if success:
                self.contacts.append(entry)
            else:
                failed += 1
            count += 1
            if print_status:
                out = "Loading ▐"
                proz = count / len(self.files)
                len1 = int(proz * 20)
                len2 = 20 - len1
                out += "█" * len1
                out += "░" * len2
                out += "▌"
                out += f" {count} / {len(self.files)} entries"
                if failed > 0:
                    out += f" ({failed} failed)"
                if len(out) > max_out_len:
                    max_out_len = len(out)
                print(out, end="\r")
        if print_status:
            print(" " * max_out_len, end="\r")
        print("Sorting ...", end="\r")
        self.contacts.sort(key = lambda e: e.display()[0].lower())
        print(f"Loaded {len(self.contacts)} Contacts.  {datetime.datetime.now()}")

    def search(self, search_str:str) -> list:
        """Returns a list of entries matching the search string.

        Args:
            search_str (str): A string to search possible flags: "all:", "#all:", "org:", "add:", "#add:", "#:", "@:"

        Returns:
            list: Sorted list of entries
        """
        result = [entry for entry in self.contacts if entry.match(search_str)]
        return result

    def add_new_entry(self, first_name:str="", last_name:str="") -> Entry:
        """Adds a new entry to the database.

        Returns:
            Entry: the newly added entry
        """
        try:
            new = Entry()
            new.personals.first_name = first_name
            new.personals.last_name = last_name
            try:
                print("Please enter the data for the new entry ...")
                print("Use ^A to to abort the entry creation or ^E to exit and save.")
                new.edit()
                if input_bool("Enter Details? (yN) ", "y", "n"):
                    new.edit_details()
            except InputExitException:
                pass
            if not new.is_empty():
                new.save()
                self.contacts.append(new)
                print("New entry added.")
                return new
        except InputAbortException:
            print("!Action Aborted!\nNo new entry was added.")
            return None

    def update_deleted_entries(self) -> None:
        """Removes all entries from the contacts list that where deleted in the file system.
        """
        killables = []
        for entry in self.contacts:
            if not isfile(entry.file):
                killables.append(entry)
        for entry in killables:
            if entry in self.contacts:
                self.contacts.remove(entry)

    def generate_random_entries(self):
        """Generates random Entries based on a random-names.txt file.
        For each line one entry will be created with a random phone number
        and an email created from the two, space seperated, names using the start letter of the first name
        a periot and the last name folowed by a random number @example.com
        Genders will also be randomized.
        """
        try:
            with open("random-names.txt", "r", encoding="utf-8") as names_file:
                while True:
                    line:str = names_file.readline().replace("\n", "").replace("\r", "").strip()
                    if line == "":
                        break
                    new = Entry()
                    names = line.split(" ")
                    new.personals.first_name = names[0]
                    new.personals.last_name = names[1]
                    new.personals.birthday = datetime.date(rnd.randrange(1960, 2008), rnd.randrange(1, 13), rnd.randrange(1, 29))
                    new.personals.male = rnd.choice([True, False])
                    new.personals.title = rnd.choice(["","","","Dr.","Prof.","Ing.","",""])
                    new.private.phone = "0" + str(rnd.randrange(1000000000, 1999999999))
                    new.private.email = (names[0][0] + "." + names[1] + str(rnd.randrange(10, 9999)) + "@example.com").lower()
                    new.save()
                    self.contacts.append(new)
        except (PermissionError, FileExistsError) as ex:
            print(ex)
