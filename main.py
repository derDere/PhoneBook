from database import *
from contact import *
from inputLib import *


def main():
    db = Database()
    print(db.folder)
    print(db.files)
    c = Contact()
    c.save()


if __name__ == "__main__":
    main()