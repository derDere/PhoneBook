"""Contains Classes holding contact informations.

   Classes:
    - Contact
    - Address
"""
import json
import os
from datetime import date
from os.path import exists, isfile
import path_config
from input_lib import input_rex, input_date, input_bool, input_multiline, PHONE_NR_PATTERN, EMAIL_PATTERN, InputExitException, HelpOutput


class Address():
    """Holds a comon address
    """
    street:str = ""
    number:str = ""
    zip_code:str = ""
    city:str = ""
    state:str = ""
    country:str = ""

    def __init__(
        self,
        street:str = "",
        number:str = "",
        zip_code:str = "",
        city:str = "",
        state:str = "",
        country:str = ""
    ) -> None:
        self.street:str = street
        self.number:str = number
        self.zip_code:str = zip_code
        self.city:str = city
        self.state:str = state
        self.country:str = country

    def fix_street(self) -> None:
        """Fixes the street name
        """
        if self.street.lower().strip().endswith("str"):
            self.street = self.street + "aße"
        elif self.street.lower().strip().endswith("str."):
            self.street = self.street[:-1] + "aße"

    def is_empty(self):
        """Checks if the address has at least one filled attribute.

        Returns:
            bool: True if no attribute was filled.
        """
        check = [
            self.street.strip() != "",
            self.number.strip() != "",
            self.zip_code.strip() != "",
            self.city.strip() != "",
            self.state.strip() != "",
            self.country.strip() != ""
        ]
        if True in check:
            return False
        return True

    def to_dict(self) -> dict:
        """Returns the object as an dictionary
        """
        return {
            "street": self.street,
            "number": self.number,
            "zip_code": self.zip_code,
            "city": self.city,
            "state": self.state,
            "country": self.country
        }

    @staticmethod
    def from_dict(dictionary) -> None:
        """Reads data from a dict into the object
        """
        addr = Address()
        addr.street = dictionary["street"]
        addr.number = dictionary["number"]
        addr.zip_code = dictionary["zip_code"]
        addr.city = dictionary["city"]
        addr.state = dictionary["state"]
        addr.country = dictionary["country"]

        return addr


class Personals():
    """Holds all personal informations
    """

    first_name:str = ""
    last_name:str = ""
    title:str = ""
    nickname:str = ""
    organisation:str = ""
    birthday:date = date(1800,1,1)
    male:bool = True

    def __init__(
        self,
        first_name:str = "",
        last_name:str = "",
        title:str = "",
        nickname:str = "",
        organisation:str = "",
        birthday:date = date(1800,1,1),
        male:bool = True
    ) -> None:
        self.first_name:str = first_name
        self.last_name:str = last_name
        self.title:str = title
        self.nickname:str = nickname
        self.organisation:str = organisation
        self.birthday:date = birthday
        self.male:bool = male

    def to_dict(self) -> dict:
        """Returns the object as an dictionary
        """
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "title": self.title,
            "nickname": self.nickname,
            "organisation": self.organisation,
            "birthday": [
                self.birthday.year,
                self.birthday.month,
                self.birthday.day
            ],
            "male": self.male
        }

    def is_empty(self):
        """Checks if the personal informations have at least one filled attribute.
        (Ignores the Gerner attribute)

        Returns:
            bool: True if no attribute was filled.
        """
        check = [
            self.first_name.strip() != "",
            self.last_name.strip() != "",
            self.title.strip() != "",
            self.nickname.strip() != "",
            self.organisation.strip() != "",
            self.birthday != date(1800,1,1)
        ]
        if True in check:
            return False
        return True

    @staticmethod
    def from_dict(dictionary) -> any:
        """Reads data from a dict into the object
        """
        pers = Personals()
        pers.first_name = dictionary["first_name"]
        pers.last_name = dictionary["last_name"]
        pers.title = dictionary["title"]
        pers.nickname = dictionary["nickname"]
        pers.organisation = dictionary["organisation"]
        pers.birthday = date(dictionary["birthday"][0], dictionary["birthday"][1], dictionary["birthday"][2])
        pers.male = bool(dictionary["male"])

        return pers


class Contact():
    """Hold contact informations
    """

    phone:str = ""
    mobile:str = ""
    fax:str = ""
    email:str = ""
    address:Address = None

    def __init__(
        self,
        phone:str = "",
        mobile:str = "",
        fax:str = "",
        email:str = "",
        address:Address = None
    ) -> None:
        self.phone:str = phone
        self.mobile:str = mobile
        self.fax:str = fax
        self.email:str = email
        self.address:Address = address

    def to_dict(self) -> dict:
        """Returns the object as an dictionary
        """
        return {
            "phone": self.phone,
            "mobile": self.mobile,
            "fax": self.fax,
            "email": self.email,
            "address": self.address.to_dict()
        }

    def is_empty(self):
        """Checks if the contact has at least one filled attribute.

        Returns:
            bool: True if no attribute was filled.
        """
        check = [
            self.mobile.strip() != "",
            self.email.strip() != "",
            self.phone.strip() != "",
            self.fax.strip() != "",
            not self.address.is_empty()
        ]
        if True in check:
            return False
        return True

    @staticmethod
    def from_dict(dictionary) -> any:
        """Reads data from a dict into the object
        """
        contact = Contact()
        contact.phone = dictionary["phone"]
        contact.mobile = dictionary["mobile"]
        contact.fax = dictionary["fax"]
        contact.email = dictionary["email"]
        contact.address = Address.from_dict(dictionary["address"])

        return contact


class Entry:
    """Representing one entry inside of a phonebook holding its informations.
    """

    def __init__(self) -> None:
        self.file = path_config.new_file_name()
        self.personals = Personals()
        self.private = Contact(address=Address())
        self.work = Contact(address=Address())
        self.notes = []

    @staticmethod
    def load(file:str) -> tuple:
        """Loads a Entry object from a file.

        Args:
            file (str): Path the the file containing the entry data.

        Returns:
            tuple: The Entry object, A bool value returning True on a successfull load
        """
        try:
            if exists(file):
                with open(file, "r", encoding="utf-8") as iofile:
                    dictionary = json.load(iofile)
                    entry = Entry()
                    entry.file = file
                    entry.personals = Personals.from_dict(dictionary["personals"])
                    entry.private = Contact.from_dict(dictionary["private"])
                    entry.work = Contact.from_dict(dictionary["work"])
                    entry.notes = dictionary["notes"]
                return (entry, True)
            return (FileNotFoundError(file), False)
        except PermissionError as ex:
            print("Entry.load")
            print(ex)
            return (ex, False)

    def reload(self) -> None:
        """Reloads the entry data from its file.
        """
        try:
            if exists(self.file):
                with open(self.file, "r", encoding="utf-8") as iofile:
                    dictionary = json.load(iofile)
                    self.personals = Personals.from_dict(dictionary["personals"])
                    self.private = Contact.from_dict(dictionary["private"])
                    self.work = Contact.from_dict(dictionary["work"])
                    self.notes = dictionary["notes"]
        except PermissionError as ex:
            print("Entry.reload")
            print(ex)

    def delete_file(self):
        """Deletes the entry file inside the file system.
        """
        if isfile(self.file):
            os.remove(self.file)

    def save(self) -> bool:
        """Saves the Entry object to the file.
        """
        try:
            with open(self.file, "w+", encoding="utf-8") as file:
                json.dump({
                    "personals": self.personals.to_dict(),
                    "private": self.private.to_dict(),
                    "work": self.work.to_dict(),
                    "notes": self.notes
                }, file)
            return True
        except PermissionError as ex:
            print("Entry.save")
            print(ex)
            return False

    def print(self) -> None:
        """Displays the entry.┌└│
        """
        display, icon = self.display()

        print( "┌────┬───────────────────────────────────────────────────────────────────")
        print(f"│ {icon} │ {display}")
        print( "├────┴───────────────────────────────────────────────────────────────────")

        if not self.personals.is_empty():
            print("│")
            if self.personals.organisation.strip() != "":
                print("│   Orginasation: " + self.personals.organisation.strip())
            if self.personals.birthday != date(1800,1,1):
                print("│   Birthday:     " + str(self.personals.birthday).strip())
            print("│")

        if not self.private.is_empty():
            print("│   Private:")
            if self.private.email.strip() != "":
                print("│      📧 E-Mail:   " + self.private.email.strip())
            if self.private.phone.strip() != "":
                print("│      📞 Phone:    " + self.private.phone.strip())
            if self.private.mobile.strip() != "":
                print("│      📱 Mobile:   " + self.private.mobile.strip())
            if self.private.fax.strip() != "":
                print("│      📠 Fax:      " + self.private.fax.strip())
            if not self.private.address.is_empty():
                print("│      🏠 Addresse: ")
                print(f"│           {self.private.address.street.strip()} {self.private.address.number.strip()}")
                print(f"│           {self.private.address.zip_code.strip()}, {self.private.address.city.strip()}")
                if self.private.address.state.strip() != "" or self.private.address.country.strip() != "":
                    print(f"│           {self.private.address.state.strip()}, {self.private.address.country.strip()}")

        if not self.work.is_empty():
            print("│   Work:")
            if self.work.email.strip() != "":
                print("│      📧 E-Mail:   " + self.work.email.strip())
            if self.work.phone.strip() != "":
                print("│      📞 Phone:    " + self.work.phone.strip())
            if self.work.mobile.strip() != "":
                print("│      📱 Mobile:   " + self.work.mobile.strip())
            if self.work.fax.strip() != "":
                print("│      📠 Fax:      " + self.work.fax.strip())
            if not self.work.address.is_empty():
                print("│      🏭 Addresse: ")
                print(f"│           {self.work.address.street.strip()} {self.work.address.number.strip()}")
                print(f"│           {self.work.address.zip_code.strip()}, {self.work.address.city.strip()}")
                if self.work.address.state.strip() != "" or self.work.address.country.strip() != "":
                    print(f"│           {self.work.address.state.strip()}, {self.work.address.country.strip()}")

        if "".join(self.notes).strip().replace(" ", "") != "":
            print("│   Notes:")
            for line in self.notes:
                if line.strip() == "":
                    line = " -"
                print("│      " + line.strip().replace("\n",""))

        print("│")
        print("└────────────────────────────────────────────────────────────────────────")

    def edit(self) -> None:
        """Edits the entry on a basic level.
        """
        try:
            print("Personals:")
            self.personals.first_name = input_rex(" - First name%s: ", default=self.personals.first_name,
                                                    show_default=(self.personals.first_name.strip() != "")).strip()
            self.personals.last_name = input_rex(" - Last name%s: ", default=self.personals.last_name,
                                                    show_default=(self.personals.last_name.strip() != "")).strip()
            self.private.mobile = input_rex(" - Mobile%s: ", "Please enter a valid mobile number!",
                                                    PHONE_NR_PATTERN, self.private.mobile, show_default=(self.private.mobile.strip() != "")).strip()
            self.private.email = input_rex(" - E-Mail%s: ", "Please enter a valid E-Mail address!",
                                                    EMAIL_PATTERN, self.private.email, show_default=(self.private.email.strip() != "")).strip()
        except InputExitException:
            pass

    def edit_note(self) -> None:
        """Edits the Contacts Note.
        """
        display, icon = self.display()
        with HelpOutput(
            lambda:
                print(
                    " To add new lines just enter some text. To change a line enter the\n" +
                    " line number and the new text it should have. If you wish to delete\n" +
                    " a line, enter the line number folowed by ^D\n" +
                    " To finish enter ^X or enter ^A to abort and discard all changes.\n" +
                    "─────────────────────────────────────────────────────────────────────────"
                )
            ):
            self.notes = input_multiline(
                icon + " " + display + " - Notes:\n─────────────────────────────────────────────────────────────────────────",
                self.notes,
                "─────────────────────────────────────────────────────────────────────────",
                True,
                " ", " │ ", "",
                "                           ... empty ..."
            )

    def edit_details(self) -> None:
        """Edits the entry details.
        """
        try:
            print("Personals:")
            self.personals.title = input_rex(" - Title%s: ", default=self.personals.title,
                                                    show_default=(self.personals.title.strip() != "")).strip()
            self.personals.nickname = input_rex(" - Nickname%s: ", default=self.personals.nickname,
                                                    show_default=(self.personals.nickname.strip() != "")).strip()
            self.personals.organisation = input_rex(" - Organisation%s: ", default=self.personals.organisation,
                                                    show_default=(self.personals.organisation.strip() != "")).strip()
            self.personals.birthday = input_date(" - Birthday%s: ", default=self.personals.birthday,
                                                    show_default=(self.personals.birthday != date(1800,1,1)))
            self.personals.male = input_bool(" - Gender%s: ", "m", "f", default=self.personals.male, show_default=True)

            print("Private:")
            self.private.phone = input_rex(" - Phone%s: ", "Please enter a valid phone number!", PHONE_NR_PATTERN,
                                                    self.private.phone, show_default=(self.private.phone.strip() != "")).strip()
            self.private.fax = input_rex(" - Fax%s: ", "Please enter a valid fax number!", PHONE_NR_PATTERN,
                                                    self.private.fax, show_default=(self.private.fax.strip() != "")).strip()

            print(" - Address:")
            self.private.address.street = input_rex("    - Street%s: ", default=self.private.address.street,
                                                    show_default=(self.private.address.street.strip() != "")).strip()
            self.private.address.fix_street()
            self.private.address.number = input_rex("    - House Number%s: ", default=self.private.address.number,
                                                    show_default=(self.private.address.number.strip() != "")).strip()
            self.private.address.zip_code = input_rex("    - Zip Code%s: ", default=self.private.address.zip_code,
                                                    show_default=(self.private.address.zip_code.strip() != "")).strip()
            self.private.address.city = input_rex("    - City%s: ", default=self.private.address.city,
                                                    show_default=(self.private.address.city.strip() != "")).strip()
            self.private.address.state = input_rex("    - State%s: ", default=self.private.address.state,
                                                    show_default=(self.private.address.state.strip() != "")).strip()
            self.private.address.country = input_rex("    - Country%s: ", default=self.private.address.country,
                                                    show_default=(self.private.address.country.strip() != "")).strip()

            print("Work:")
            self.work.email = input_rex(" - E-Mail%s: ", "Please enter a valid E-Mail address!", EMAIL_PATTERN, self.work.email,
                                                    show_default=(self.work.email.strip() != "")).strip()
            self.work.mobile = input_rex(" - Mobile%s: ", "Please enter a valid mobile number!", PHONE_NR_PATTERN, self.work.mobile,
                                                    show_default=(self.work.mobile.strip() != "")).strip()
            self.work.phone = input_rex(" - Phone%s: ", "Please enter a valid phone number!", PHONE_NR_PATTERN, self.work.phone,
                                                    show_default=(self.work.phone.strip() != "")).strip()
            self.work.fax = input_rex(" - Fax%s: ", "Please enter a valid fax number!", PHONE_NR_PATTERN, self.work.fax,
                                                    show_default=(self.work.fax.strip() != "")).strip()

            print(" - Address:")
            self.work.address.street = input_rex("    - Street%s: ", default=self.work.address.street,
                                                    show_default=(self.work.address.street.strip() != "")).strip()
            self.work.address.fix_street()
            self.work.address.number = input_rex("    - House Number%s: ", default=self.work.address.number,
                                                    show_default=(self.work.address.number.strip() != "")).strip()
            self.work.address.zip_code = input_rex("    - Zip Code%s: ", default=self.work.address.zip_code,
                                                    show_default=(self.work.address.zip_code.strip() != "")).strip()
            self.work.address.city = input_rex("    - City%s: ", default=self.work.address.city,
                                                    show_default=(self.work.address.city.strip() != "")).strip()
            self.work.address.state = input_rex("    - State%s: ", default=self.work.address.state,
                                                    show_default=(self.work.address.state.strip() != "")).strip()
            self.work.address.country = input_rex("    - Country%s: ", default=self.work.address.country,
                                                    show_default=(self.work.address.country.strip() != "")).strip()
        except InputExitException:
            pass

    def display(self) -> str:
        """Returns a displayable name

        Returns:
            (str, str): [[Nickname] FirstName LastName] and a fitting icon
        """
        icon = "👨"
        if not self.personals.male:
            icon = "👩"
        display = ""
        if self.personals.nickname.strip() != "":
            display = self.personals.nickname
            display += ", "
        if self.personals.title.strip() != "":
            display += self.personals.title
            display += " "
        display += self.personals.first_name
        display += " "
        display += self.personals.last_name
        return (display, icon)

    def get_contact(self) -> str:
        """Return the first filled contact information prioritiesed in the following order:
        private-mobile, private-phone, work-mobile, work-phone, private-email, work-email, private-fax, work-fax

        Returns:
            (str, str): the first found contact information of this entry and an icon fitting it
        """
        result = ""
        icon = ""
        if self.private.mobile.strip() != "":
            icon = "📱"
            result = self.private.mobile.strip()
        elif self.private.phone.strip() != "":
            icon = "📞"
            result = self.private.phone.strip()
        elif self.work.mobile.strip() != "":
            icon = "📱"
            result = self.work.mobile.strip()
        elif self.work.phone.strip() != "":
            icon = "📞"
            result = self.work.phone.strip()
        elif self.private.email.strip() != "":
            icon = "📧"
            result = self.private.email.strip()
        elif self.work.email.strip() != "":
            icon = "📧"
            result = self.work.email.strip()
        elif self.private.fax.strip() != "":
            icon = "📠"
            result = self.private.fax.strip()
        elif self.work.fax.strip() != "":
            icon = "📠"
            result = self.work.fax.strip()
        return (result, icon)

    def is_empty(self):
        """Checks if the entry has at least one filled attribute.
           (Gender attribute is ignored!)

        Returns:
            bool: True if no attribute was filled.
        """
        check = [
            self.personals.first_name.strip() != "",
            self.personals.last_name.strip() != "",
            self.private.mobile.strip() != "",
            self.private.email.strip() != "",
            self.personals.title.strip() != "",
            self.personals.nickname.strip() != "",
            self.personals.organisation.strip() != "",
            self.personals.birthday != date(1800,1,1),
            self.private.phone.strip() != "",
            self.private.fax.strip() != "",
            self.private.address.street.strip() != "",
            self.private.address.number.strip() != "",
            self.private.address.zip_code.strip() != "",
            self.private.address.city.strip() != "",
            self.private.address.state.strip() != "",
            self.private.address.country.strip() != "",
            self.work.email.strip() != "",
            self.work.mobile.strip() != "",
            self.work.phone.strip() != "",
            self.work.fax.strip() != "",
            self.work.address.street.strip() != "",
            self.work.address.number.strip() != "",
            self.work.address.zip_code.strip() != "",
            self.work.address.city.strip() != "",
            self.work.address.state.strip() != "",
            self.work.address.country.strip() != ""
        ]
        if True in check:
            return False
        return True

    def match(self, search_str:str) -> bool:
        """Checks if the entry matches the search
        """
        search_str = search_str.lower()
        parts = []

        if search_str.startswith("all:") or search_str.startswith("#all:"):
            parts.append(self.personals.organisation.lower())
            parts.append(self.private.address.city.lower())
            parts.append(self.private.address.country.lower())
            parts.append(self.private.address.state.lower())
            parts.append(self.private.address.street.lower())
            parts.append(self.work.address.city.lower())
            parts.append(self.work.address.country.lower())
            parts.append(self.work.address.state.lower())
            parts.append(self.work.address.street.lower())
            parts.append(self.private.email.lower())
            parts.append(self.work.email.lower())

            if search_str.startswith("#all:"):
                parts.append(str(self.private.address.number).lower())
                parts.append(str(self.private.address.zip_code).lower())
                parts.append(str(self.work.address.number).lower())
                parts.append(str(self.work.address.zip_code).lower())
                parts.append(str(self.private.phone).lower())
                parts.append(str(self.private.mobile).lower())
                parts.append(str(self.private.fax).lower())
                parts.append(str(self.work.phone).lower())
                parts.append(str(self.work.mobile).lower())
                parts.append(str(self.work.fax).lower())
                search_str = search_str[5:]
            else:
                search_str = search_str[4:]

        elif search_str.startswith("org:"):
            parts.append(self.personals.organisation.lower())
            search_str = search_str[4:]

        elif search_str.startswith("add:") or search_str.startswith("#add:"):
            parts.append(self.private.address.city.lower())
            parts.append(self.private.address.country.lower())
            parts.append(self.private.address.state.lower())
            parts.append(self.private.address.street.lower())
            parts.append(self.work.address.city.lower())
            parts.append(self.work.address.country.lower())
            parts.append(self.work.address.state.lower())
            parts.append(self.work.address.street.lower())

            if search_str.startswith("#add:"):
                parts.append(str(self.private.address.number).lower())
                parts.append(str(self.private.address.zip_code).lower())
                parts.append(str(self.work.address.number).lower())
                parts.append(str(self.work.address.zip_code).lower())
                search_str = search_str[5:]
            else:
                search_str = search_str[4:]

        elif search_str.startswith("@:"):
            parts.append(self.private.email.lower())
            parts.append(self.work.email.lower())
            search_str = search_str[2:]

        elif search_str.startswith("#:"):
            parts.append(str(self.private.phone).lower())
            parts.append(str(self.private.mobile).lower())
            parts.append(str(self.private.fax).lower())
            parts.append(str(self.work.phone).lower())
            parts.append(str(self.work.mobile).lower())
            parts.append(str(self.work.fax).lower())
            search_str = search_str[2:]

        else:
            parts.append(self.personals.first_name.lower())
            parts.append(self.personals.last_name.lower())
            parts.append(self.personals.nickname.lower())

        for part in parts:
            if search_str in part:
                return True

        return False
