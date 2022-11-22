from datetime import date

from os.path import expanduser

class Contact:

    def __init__(self) -> None:
        """
        self.file = ""

        self.firstName = ""
        self.lastName = ""
        self.title = ""
        self.nikname = ""
        self.organisation = ""
        self.birthday:date = date()
        self.male = True

        self.phonePrivat = ""
        self.mobilePrivat = ""
        self.faxPrivat = ""
        self.emailPrivat = ""
        self.addressPrivat:Address = None

        self.phoneWork = ""
        self.mobileWork = ""
        self.faxWork = ""
        self.emailWork = ""
        self.addressWork:Address = None

        self.notes = ""
        """
        self.file = expanduser("/mnt/e/test.vcf")

        self.firstName = "Max"
        self.lastName = "Musterman"
        self.title = "Herr"
        self.nikname = "Maxi"
        self.organisation = "REWE"
        self.birthday:date = date(1992,3,8)
        self.male = True

        self.phonePrivat = "+492173149623"
        self.mobilePrivat = "01224565543"
        self.faxPrivat = "320805"
        self.emailPrivat = "maxi69@gmail.com"
        self.addressPrivat:Address = Address("Hasenstrasse","55A","51268","Bielefeld","NRW","Deutschland")

        self.phoneWork = "6754324456"
        self.mobileWork = "3245678756453"
        self.faxWork = "354643334"
        self.emailWork = "mustermann@rewe.de"
        self.addressWork:Address = Address("Stadtmitte","1a","553479","Köln","NEW", "Austria")

        self.notes = "Ist ein echtes Musterbeispiel!\nVerstehste?!"

    def Load(file:str) -> tuple:
        return (Contact(file), True)
    
    def save(self):

        #ERRORS
        #Save ist invalid
        #Check https://vcardmaker.com/

        with open(self.file, "w+") as f:
            
            f.write("BEGIN:VCARD\n")
            f.write("VERSION:4.0\n")
            f.write("PROFILE:VCARD\n")
            
            f.write("N:%s;%s;;;%s\n" % (self.lastName, self.firstName, self.title))
            f.write("FN:%s\n" % self.nikname)
            f.write("ORG:%s\n" % self.organisation)
            f.write("BDAY:--%02i%02i\n" % (self.birthday.month, self.birthday.day))
            if self.male: f.write("GENDER:M\n")
            else: f.write("GENDER:F\n")
            
            f.write("TEL;TYPE=VOICE,HOME;VALUE#uri:tel:%s\n" % self.phonePrivat)
            f.write("TEL;TYPE=CELL,HOME;VALUE#uri:tel:%s\n" % self.mobilePrivat)
            f.write("TEL;TYPE=FAX,HOME;VALUE#uri:tel:%s\n" % self.faxPrivat)
            f.write("EMAIL;TYPE=HOME:%s\n" % self.emailPrivat)
            f.write("ADR;TYPE=HOME:;;%s %s;%s;%s;%s;%s\n" % (
                self.addressPrivat.street,
                self.addressPrivat.number,
                self.addressPrivat.city,
                self.addressPrivat.state,
                self.addressPrivat.zipCode,
                self.addressPrivat.country
            ))
            
            f.write("TEL;TYPE=VOICE,WORK;VALUE#uri:tel:%s\n" % self.phoneWork)
            f.write("TEL;TYPE=CELL,WORK;VALUE#uri:tel:%s\n" % self.mobileWork)
            f.write("TEL;TYPE=FAX,WORK;VALUE#uri:tel:%s\n" % self.faxWork)
            f.write("EMAIL;TYPE=WORK:%s\n" % self.emailWork)
            f.write("ADR;TYPE=WORK:;;%s %s;%s;%s;%s;%s\n" % (
                self.addressWork.street,
                self.addressWork.number,
                self.addressWork.city,
                self.addressWork.state,
                self.addressWork.zipCode,
                self.addressWork.country
            ))
            
            f.write("NOTE:%s\n" % self.notes.replace("\n","\\n"))

            f.write("END:VCARD\n")


class Address:

    def __init__(self, street:str="", number:str="", zipCode:str="", city:str="", state:str="", country:str="") -> None:
        self.street = street
        self.number = number
        self.zipCode = zipCode
        self.city = city
        self.state = state
        self.country = country