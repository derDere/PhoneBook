"""Contains Classes holding contact informations.

   Classes:
    - Contact
    - Address
"""
import json
from datetime import date
from os.path import exists
import path_config
from input_lib import input_rex, input_date, input_bool, PHONE_NR_PATTERN, EMAIL_PATTERN


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
        self.notes = ""

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
                return (entry, True)
            else:
                return (FileNotFoundError(file), False)
        except Exception as ex:
            print("Entry.load")
            print(ex)
            return (ex, False)

    def save(self) -> bool:
        """Saves the Entry object to the file.
        """
        try:
            with open(self.file, "w+", encoding="utf-8") as file:
                json.dump({
                    "personals": self.personals.to_dict(),
                    "private": self.private.to_dict(),
                    "work": self.work.to_dict()
                }, file)
            return True
        except Exception as ex:
            print("Entry.save")
            print(ex)
            return False

    def print(self) -> None:
        """Displays the entry.
        """
        string = json.dumps({
                    "personals": self.personals.to_dict(),
                    "private": self.private.to_dict(),
                    "work": self.work.to_dict()
                }, indent=2)
        print(string)

    def edit(self) -> None:
        """Edits the entry on a basic level.
        """
        print("Personals:")
        self.personals.first_name = input_rex(" - First name%s: ", default=self.personals.first_name, show_default=(self.personals.first_name.strip() != "")).strip()
        self.personals.last_name = input_rex(" - Last name%s: ", default=self.personals.last_name, show_default=(self.personals.last_name.strip() != "")).strip()
        self.private.mobile = input_rex(" - Mobile%s: ", "Please enter a valid mobile number!", PHONE_NR_PATTERN, self.private.mobile, show_default=(self.private.mobile.strip() != "")).strip()
        self.private.email = input_rex(" - E-Mail%s: ", "Please enter a valid E-Mail address!", EMAIL_PATTERN, self.private.email, show_default=(self.private.email.strip() != "")).strip()

    def edit_details(self) -> None:
        """Edits the entry details.
        """
        print("Personals:")
        self.personals.title = input_rex(" - Title%s: ", default=self.personals.title, show_default=(self.personals.title.strip() != "")).strip()
        self.personals.nickname = input_rex(" - Nickname%s: ", default=self.personals.nickname, show_default=(self.personals.nickname.strip() != "")).strip()
        self.personals.organisation = input_rex(" - Organisation%s: ", default=self.personals.organisation, show_default=(self.personals.organisation.strip() != "")).strip()
        self.personals.birthday = input_date(" - Birthday%s: ", default=self.personals.birthday, show_default=(self.personals.birthday != date(1800,1,1)))
        self.personals.male = input_bool(" - Gender%s: ", "m", "f", default=self.personals.male, show_default=True)

        print("Private:")
        self.private.phone = input_rex(" - Phone%s: ", "Please enter a valid phone number!", PHONE_NR_PATTERN, self.private.phone, show_default=(self.private.phone.strip() != "")).strip()
        self.private.fax = input_rex(" - Fax%s: ", "Please enter a valid fax number!", PHONE_NR_PATTERN, self.private.fax, show_default=(self.private.fax.strip() != "")).strip()

        print(" - Address:")
        self.private.address.street = input_rex("    - Street%s: ", default=self.private.address.street, show_default=(self.private.address.street.strip() != "")).strip()
        self.private.address.fix_street()
        self.private.address.number = input_rex("    - House Number%s: ", default=self.private.address.number, show_default=(self.private.address.number.strip() != "")).strip()
        self.private.address.zip_code = input_rex("    - Zip Code%s: ", default=self.private.address.zip_code, show_default=(self.private.address.zip_code.strip() != "")).strip()
        self.private.address.city = input_rex("    - City%s: ", default=self.private.address.city, show_default=(self.private.address.city.strip() != "")).strip()
        self.private.address.state = input_rex("    - State%s: ", default=self.private.address.state, show_default=(self.private.address.state.strip() != "")).strip()
        self.private.address.country = input_rex("    - Country%s: ", default=self.private.address.country, show_default=(self.private.address.country.strip() != "")).strip()

        print("Work:")
        self.work.email = input_rex(" - E-Mail%s: ", "Please enter a valid E-Mail address!", EMAIL_PATTERN, self.work.email, show_default=(self.work.email.strip() != "")).strip()
        self.work.mobile = input_rex(" - Mobile%s: ", "Please enter a valid mobile number!", PHONE_NR_PATTERN, self.work.mobile, show_default=(self.work.mobile.strip() != "")).strip()
        self.work.phone = input_rex(" - Phone%s: ", "Please enter a valid phone number!", PHONE_NR_PATTERN, self.work.phone, show_default=(self.work.phone.strip() != "")).strip()
        self.work.fax = input_rex(" - Fax%s: ", "Please enter a valid fax number!", PHONE_NR_PATTERN, self.work.fax, show_default=(self.work.fax.strip() != "")).strip()

        print(" - Address:")
        self.work.address.street = input_rex("    - Street%s: ", default=self.work.address.street, show_default=(self.work.address.street.strip() != "")).strip()
        self.work.address.fix_street()
        self.work.address.number = input_rex("    - House Number%s: ", default=self.work.address.number, show_default=(self.work.address.number.strip() != "")).strip()
        self.work.address.zip_code = input_rex("    - Zip Code%s: ", default=self.work.address.zip_code, show_default=(self.work.address.zip_code.strip() != "")).strip()
        self.work.address.city = input_rex("    - City%s: ", default=self.work.address.city, show_default=(self.work.address.city.strip() != "")).strip()
        self.work.address.state = input_rex("    - State%s: ", default=self.work.address.state, show_default=(self.work.address.state.strip() != "")).strip()
        self.work.address.country = input_rex("    - Country%s: ", default=self.work.address.country, show_default=(self.work.address.country.strip() != "")).strip()

    def display(self) -> str:
        """Returns a displayable name

        Returns:
            str: [[Nickname] FirstName LastName]
        """
        display = ""
        if self.personals.nickname.strip() != "":
            display = self.personals.nickname
            display += ", "
        display += self.personals.first_name
        display += " "
        display += self.personals.last_name
        return display

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


















"""
        # OLD VCF file saving
        # Maybe another time

        #ERRORS
        #Save ist invalid
        #Check https://vcardmaker.com/

        with open(self.file, "w+") as f:

            f.write("BEGIN:VCARD\n")
            f.write("VERSION:4.0\n")
            f.write("PROFILE:VCARD\n")

            f.write(f"N:{self.personals.last_name};{self.personals.first_name};;;{self.personals.title}\n")
            f.write(f"FN:{self.personals.nikname}\n")
            f.write(f"ORG:{self.personals.organisation}\n")
            f.write(f"BDAY:--{self.personals.birthday.month:02}{self.personals.birthday.day:02}\n")
            if self.personals.male:
                f.write("GENDER:M\n")
            else:
                f.write("GENDER:F\n")

            f.write(f"TEL;TYPE=VOICE,HOME;VALUE#uri:tel:{self.private.phone}\n")
            f.write(f"TEL;TYPE=CELL,HOME;VALUE#uri:tel:{self.private.mobile}\n")
            f.write(f"TEL;TYPE=FAX,HOME;VALUE#uri:tel:{self.private.fax}\n")
            f.write(f"EMAIL;TYPE=HOME:{self.private.email}\n")
            f.write(
                f"ADR;TYPE=HOME:;;{self.private.address.street} {self.private.address.number};" +
                f"{self.private.address.city};" +
                f"{self.private.address.state};" +
                f"{self.private.address.zip_code};" +
                f"{self.private.address.country}\n"
            )

            f.write(f"TEL;TYPE=VOICE,WORK;VALUE#uri:tel:{self.work.phone}\n")
            f.write(f"TEL;TYPE=CELL,WORK;VALUE#uri:tel:{self.work.mobile}\n")
            f.write(f"TEL;TYPE=FAX,WORK;VALUE#uri:tel:{self.work.fax}\n")
            f.write(f"EMAIL;TYPE=WORK:{self.work.email}\n")
            f.write(
                f"ADR;TYPE=WORK:;;{self.work.address.street} {self.work.address.number};" +
                f"{self.work.address.city};" +
                f"{self.work.address.state};" +
                f"{self.work.address.zip_code};" +
                f"{self.work.address.country}\n"
            )

            f.write("NOTE:%s\n" % self.notes.replace("\n","\\n"))

            f.write("END:VCARD\n")
"""
