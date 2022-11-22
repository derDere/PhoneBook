"""Contains Classes holding contact informations.

   Classes:
    - Contact
    - Address
"""

import json
from datetime import date
from typing import NamedTuple
from os.path import exists
import path_config


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
    address:Address = Address()

    def __init__(
        self,
        phone:str = "",
        mobile:str = "",
        fax:str = "",
        email:str = "",
        address:Address = Address()
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
        contact.address = Address()
        contact.address.from_dict(dictionary["address"])

        return contact


class Entry:
    """Representing one entry inside of a phonebook holding its informations.
    """

    def __init__(self) -> None:
        self.file = path_config.get_path("test")

        self.personals = Personals(
            "Max",
            "Musterman",
            "Herr",
            "Maxi",
            "REWE",
            date(1992, 3, 8),
            True
        )
        self.private = Contact(
            "+492173149623",
            "01224565543",
            "320805",
            "maxi69@gmail.com",
            Address(
                "Hasenstrasse",
                "55a",
                "51268",
                "Bielefeld",
                "NRW",
                "Deutschland"
            )
        )
        self.work = Contact(
            "6754324456",
            "3245678756453",
            "354643334",
            "mustermann@rewe.de",
            Address(
                "Stadtmitte",
                "1a",
                "553479",
                "Köln",
                "NEW",
                "Austria"
            )
        )

        self.notes = "Ist ein echtes Musterbeispiel!\nVerstehste?!"

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

    def print(self):
        """Displays the entry.
        """
        string = json.dumps({
                    "personals": self.personals.to_dict(),
                    "private": self.private.to_dict(),
                    "work": self.work.to_dict()
                }, indent=2)
        print(string)


















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
