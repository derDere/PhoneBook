"""Contains Classes holding contact informations.

   Classes:
    - Contact
    - Address
"""

import json
from datetime import date
from os.path import expanduser
from typing import NamedTuple
import path_config


class Address(NamedTuple):
    """Holds a comon address
    """

    street:str
    number:str
    zip_code:str
    city:str
    state:str
    country:str

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

    def from_dict(self, dictionary):
        """Reads data from a dict into the object
        """
        self.street = dictionary["street"]
        self.number = dictionary["number"]
        self.zip_code = dictionary["zip_code"]
        self.city = dictionary["city"]
        self.state = dictionary["state"]
        self.country = dictionary["country"]


class Personals(NamedTuple):
    """Holds all personal informations
    """

    first_name:str
    last_name:str
    title:str
    nickname:str
    organisation:str
    birthday:date
    male:bool

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
            "male:": self.male
        }

    def from_dict(self, dictionary):
        """Reads data from a dict into the object
        """
        self.first_name = dictionary["first_name"]
        self.last_name = dictionary["last_name"]
        self.title = dictionary["title"]
        self.nickname = dictionary["nickname"]
        self.organisation = dictionary["organisation"]
        self.birthday = date(dictionary["birthday"][0], dictionary["birthday"][1], dictionary["birthday"][2])
        self.male = bool(dictionary["male"])


class Contact(NamedTuple):
    """Hold contact informations
    """

    phone:str
    mobile:str
    fax:str
    email:str
    address:Address

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

    def from_dict(self, dictionary):
        """Reads data from a dict into the object
        """
        self.phone = dictionary["phone"]
        self.mobile = dictionary["mobile"]
        self.fax = dictionary["fax"]
        self.email = dictionary["email"]
        self.address = Address()
        self.address.from_dict(dictionary["address"])


class Entry:
    """Representing one entry inside of a phonebook holding its informations.
    """

    def __init__(self) -> None:
        self.file = expanduser(f"{path_config.FOLDER_PATH}/test{path_config.FILE_EXTENSINON}")

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
        con = Entry()
        con.file = file
        return (con, True)

    def save(self):
        """Saves the Entry object to the file.
        """
        jsonstr = json.dumps({
            "personals": self.personals.to_dict(),
            "private": self.private.to_dict(),
            "work": self.work.to_dict()
        })

        return jsonstr


















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
