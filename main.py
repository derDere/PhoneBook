"""Main Phonebook script
"""

import os
import math
from database import Database
from entry import Entry
from input_lib import EXIT_INPUT_KEY_SEQUENCE, HELP_INPUT_KEY_SEQUENCE, input_bool, input_choice


def clear():
    """Clears the screen
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def entry_display(entry:Entry, database:Database) -> bool:
    """Displays a menu to execute action on a single entry and also displays the entry to view it.
    """
    show_help = False
    while True:
        clear()
        entry.print()
        if show_help:
            print(" Options:")
            print("   help or ?         Shows help")
            print("   edit or e         Edits the entry")
            print("   delete or d       Deletes the entry")
            print("   back or b or ^X   returns to the previous screen")
            print("   mail or m         Send an E-Mail")
            print("   tel or t          Call a phone or mobile number")
        else:
            print(" Options: help, ?, edit, e, delete, d, back, b, ^X, mail, m, tel, t")
        print("─────────────────────────────────────────────────────────────────────────")
        line = input(": ").strip().lower()

        if line in ["b", "back", EXIT_INPUT_KEY_SEQUENCE]:
            break

        elif line in ["help", "?"]:
            show_help = True

        elif line in ["mail", "m"]:
            mails = {}
            if entry.private.email.strip() != "":
                mails["Private: " + entry.private.email] = entry.private.email
            if entry.work.email.strip() != "":
                mails["Work: " + entry.work.email] = entry.work.email
            if len(mails.keys()) <= 0:
                input("No E-Mail addresses available! Press ENTER to continue ...")
            else:
                mails["Cancel"] = ""
                target_mail_add = ""
                if len(mails.keys()) > 1:
                    target_mail_add = input_choice("Choose which E-Mail to send to:", mails)
                if target_mail_add.strip() != "":
                    hyper_link = f"explorer mailto:{target_mail_add}"
                    os.system(hyper_link)
                    input("Press ENTER to continue ...")

        elif line in ["tel", "t"]:
            numbers = {}
            if entry.private.phone.strip() != "":
                numbers["Private phone: " + entry.private.phone] = entry.private.phone
            if entry.private.mobile.strip() != "":
                numbers["Private mobile: " + entry.private.mobile] = entry.private.mobile
            if entry.work.phone.strip() != "":
                numbers["Work phone: " + entry.work.phone] = entry.work.phone
            if entry.work.mobile.strip() != "":
                numbers["Work mobile: " + entry.work.mobile] = entry.work.mobile
            if len(numbers.keys()) <= 0:
                input("No Numbers to call available! Press ENTER to continue ...")
            else:
                numbers["Cancel"] = ""
                target_number = ""
                if len(numbers.keys()) > 1:
                    target_number = input_choice("Choose wich number to call:", numbers)
                if target_number.strip() != "":
                    hyper_link = f"explorer tel:{target_number}"
                    os.system(hyper_link)
                    input("Press ENTER to continue ...")

        elif line in ["edit", "e"]:
            clear()
            entry.edit()
            if input_bool("Edit Details? (yN) ", "y", "n"):
                entry.edit_details()
            entry.save()

        elif line in ["delete", "d"]:
            if input_bool("Are you sure you want to permanently delete this entry?! (delete|no) ", "delete", "no"):
                display, _ = entry.display()
                entry.delete_file()
                database.update_deleted_entries()
                print(f"Entry for \"{display}\" was deleted!")
                input("Press ENTER to return to main menu ...")
                return True
    return False


def entry_list_view(entries:list[Entry], database:Database) -> None:
    """Displays a multipaged list of entries.

    Args:
        entries (list[Entry]): The full list of entries to be shown in the paged view.
    """
    page_size = 10
    page = 0
    show_help = False
    while True:
        page_count = int(math.ceil(len(entries) / page_size))
        display_max_len = 0
        index_max_len = 0

        for i in range(page * page_size, page * page_size + page_size):
            if i < len(entries):
                entry = entries[i]
                display, dicon = entry.display()
                if len(display) > display_max_len:
                    display_max_len = len(display)
                if len(str(i+1)) > index_max_len:
                    index_max_len = len(str(i+1))

        clear()
        print("─────────────────────────────────────────────────────────────────────────")
        page_start_index = page * page_size
        page_max_index = page * page_size + page_size
        if page_max_index > len(entries):
            page_max_index = len(entries)
        print(
            f" Page: {page+1} / {page_count} - Index {(page_start_index) + 1} to {page_max_index} of {len(entries)} Entries - Page size: {page_size}"
        )
        print("─────────────────────────────────────────────────────────────────────────")
        display = "Name"
        display += " " * (display_max_len - len(display))
        index = "#"
        index = (" " * (index_max_len - len(index))) + index
        print(" [" + index + "] 👫 " + display + " 📫 Contact")
        for i in range(page_start_index, page * page_size + page_size):
            if i < len(entries):
                entry = entries[i]
                display, dicon = entry.display()
                display += " " * (display_max_len - len(display))
                contact, cicon = entry.get_contact()
                index = str(i + 1)
                index = (" " * (index_max_len - len(index))) + index
                print(" [" + index + "] " + dicon + " " + display + " " + cicon + " " + contact)
            else:
                print("-")
        print("─────────────────────────────────────────────────────────────────────────")
        if show_help:
            print(" [any number #]   view Entry with matching #-number")
            print(" n                next page")
            print(" p                previous page")
            print(" +                enlarge page size (max 200)")
            print(" -                shrink page size (min 5)")
            print(" ?                display help")
            print(" b or ^X          back to main menu")
            print()
            print(" n,p,+,- can be entered multiple times to make bigger steps.")
            show_help = False
        else:
            print(" Options: #, p, n, b, +, -, ?, ^X")
        print("─────────────────────────────────────────────────────────────────────────")
        line = input(": ").strip().lower()
        if line.isnumeric():
            i = int(line)
            i -= 1
            if page_start_index <= i < page_max_index:
                entry = entries[i]
                if entry_display(entry, database):
                    break
        elif line == "?":
            show_help = True
        elif line == "b" or line == EXIT_INPUT_KEY_SEQUENCE:
            break
        elif line[0] == "p":
            for char in line:
                if char == "p" and page > 0:
                    page -= 1
        elif line[0] == "n":
            for char in line:
                if char == "n" and page < (page_count - 1):
                    page += 1
        elif line[0] == "+":
            for char in line:
                if char == "+" and page_size < 200:
                    page_size += 1
        elif line[0] == "-":
            for char in line:
                if char == "-" and page_size > 5:
                    page_size -= 1
        page_count = int(math.ceil(len(entries) / page_size))
        if page < 0:
            page = 0
        if page >= page_count:
            page = page_count - 1


def display_help() -> None:
    """Displays the controls for the main menu.
    """
    print("Available command:")
    print("    ^X or exit                      Exit application.")
    print("    ? or help                       Display help.")
    print("    + [[first name] [last name]]    To create a new entry.")
    print("                                    (first and last name are optional.)")
    print("    [any string]                    Search entries.")
    print("    *                               List all entries.")


def print_title():
    """Prints the applications title.
    """
    print(r"   _____  _                      _                 _")
    print(r"  |  __ \| |                    | |               | |")
    print(r"  | |__) | |__   ___  _ __   ___| |__   ___   ___ | | __")
    print(r"  |  ___/| '_ \ / _ \| '_ \ / _ \ '_ \ / _ \ / _ \| |/ /")
    print(r"  | |    | | | | (_) | | | |  __/ |_) | (_) | (_) |   <")
    print(r"  |_|    |_| |_|\___/|_| |_|\___|_.__/ \___/ \___/|_|\_\ ")
    print()
    print(r"────────────────────────────────────────────────────────────")


if __name__ == "__main__":
    def main() -> None:
        """main function of this programm
        """
        clear()
        print_title()
        database = Database()
        #database.generate_random_entries()
        print()
        display_help()
        print()
        first_run = True
        show_help = False

        line = ""
        while line.lower() != "exit" and line != EXIT_INPUT_KEY_SEQUENCE:
            if not first_run:
                clear()
                print_title()
                print()
                if show_help:
                    display_help()
                    print()
                show_help = False

            first_run = False

            line = input(": ").strip()

            if line.lower() == "exit" or line == EXIT_INPUT_KEY_SEQUENCE:
                print("Exiting application ...")

            elif line.strip().startswith("+"):
                quic_first_name = ""
                quic_last_name = ""
                if len(line[1:].strip()) > 0:
                    parts = line[1:].strip().split(" ")
                    if len(parts) >= 1:
                        quic_first_name = parts[0]
                    if len(parts) >= 2:
                        quic_last_name = parts[1]
                database.add_new_entry(quic_first_name,quic_last_name)

            elif line.lower() == "help" or line == HELP_INPUT_KEY_SEQUENCE:
                show_help = True

            elif line.strip() == "*":
                if len(database.contacts) > 1:
                    entry_list_view(database.contacts, database)
                elif len(database.contacts) == 1:
                    entry_display(database.contacts[0], database)
                else:
                    print("\nCurrently your phonebook is empty 🤷‍♂️ ...\n")
                    input("Press ENTER to continue ...")

            elif line.strip() != "":
                search_result = database.search(line)
                if len(search_result) > 1:
                    entry_list_view(search_result, database)
                elif len(search_result) == 1:
                    entry_display(search_result[0], database)
                else:
                    print("\nNo results ...\n")
                    input("Press ENTER to continue ...")

    ##############################################
    main()
