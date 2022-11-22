"""Contains Classes holding contact informations.

   Classes:
    - Contact
    - Address
"""

from collections import namedtuple
from datetime import date
from os.path import expanduser


Address = namedtuple("Address", "street:str number:str zip_code:str city:str state:str country:str")
Personals = namedtuple("Personals", "first_name:str last_name:str title:str nickname:str organisation:str birthday:date male:bool")
Contact = namedtuple("Contact", "phone:str mobile:str fax:str email:str address:Address")


class Entry:
    """Representing one entry inside of a phonebook holding its informations.
    """

    def __init__(self) -> None:
        self.file = expanduser("/mnt/e/test.vcf")

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
