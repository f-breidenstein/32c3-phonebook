#! /usr/bin/env python3
import requests
from bs4 import BeautifulSoup

URL = "https://eventphone.de/guru2/phonebook?event=32C3&all=1"
FILENAME = "32c3.vcf"

def create_vcard_dect(nick, number):
    return "BEGIN:VCARD\nVERSION:3.0\nN:{nick};;;\nFN:{nick}\nTEL;HOME:{number}\nEND:VCARD\n".format(nick=nick, number=number)

def main():
    vcard = ""
    print("Crawling the site")
    r = requests.get(URL)
    pool = BeautifulSoup(r.text, "lxml")
    phonebook = pool.find('table', { "class" : "table t1" })
    entrys = phonebook.findAll('tr')
    print("Extracting the people")
    for person in entrys:
        entry = [e.text for e in person.findAll('td')]
        try:
            number, nick, phonetype, position = entry
            vcard = "{}{}".format(vcard, create_vcard(nick, number))
        except:
            pass
    print("Write to file")
    with open(FILENAME, "w") as f:
        f.write(vcard)
    print("Finished!")

if __name__ == "__main__":
    main()
