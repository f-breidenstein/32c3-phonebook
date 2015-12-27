#! /usr/bin/env python3
import requests
from bs4 import BeautifulSoup

URL = "https://eventphone.de/guru2/phonebook?event=32C3&all=1"
FILENAME = "32c3.vcf"

def create_vcard_dect(nick, number):
    text = "BEGIN:VCARD\nVERSION:3.0\nN:{nick};;;\nFN:{nick}\nTEL;HOME:{number}\nEND:VCARD\n".format(nick=nick, number=number)
    return text


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
            number = entry[0]
            nick = entry[1]
            phonetype = entry[2]
            position = entry[3]
            vcard = "{}{}".format(vcard, create_vcard(nick, number))
        except:
            pass
    print("Write to file")
    text_file = open(FILENAME, "w")
    text_file.write(vcard)
    text_file.close()
    print("Finished!")


if __name__ == "__main__":
    main()
