#!/usr/bin/env python3

import sqlite3
import sys

class Contact:
    def __init__(self):
        self.conn = sqlite3.connect('contact.db')
        self.c = self.conn.cursor()

    def add(self):
        name = input('Please input name: ')
        phone_num = int(input('Please input phone_num: '))
        other = input('Other messages?(optional) ')

        contant = (name, phone_num, other)
        self.c.execute("INSERT INTO CONTACT VALUES(?, ?, ?)", contant)
        self.conn.commit()

        print('info added')

    def search(self):
        query = input('What do you want to search? ')
        query = (query, query, query)
        self.c.execute("SELECT * FROM CONTACT WHERE NAME = ? OR PHONE_NUM = ? OR OTHER = ?", query)

        print(self.c.fetchone())

    def delete(self):
        query = input('Who do you want to forget? ')

        self.c.execute("SELECT * FROM CONTACT WHER NAME = ?", (query,))
        print(self.c.fetchone())

        ask = input("Do you want to forget him/her? tell me (yes) or (no)")
        if ask == 'yes' or 'Yes' or 'YES':
            self.c.execute("DELETE FROM CONTACT WHERE NAME = ?", (query,))
            self.conn.commit()
            print('You just have forgotten someone')

        elif ask == 'no' or 'No' or 'NO':
            print("You still can't forget him/her, right?")

    def update(self):
        name = input('You have new info about who? ')
        new_contant = input('What do you want to update, name, phone or other? ')

        if new_contant == 'name':
            new_name = input('tell me new name ')
            self.c.execute("UPDATE CONTACT SET NAME = ? WHERE NAME = ?", (new_name, name))

        elif new_contant == 'phone':
            new_ph_num = input('tell me new phone number: ')
            self.c.execute("UPDATE CONTACT SET PHONE_NUM = ? WHERE NAME = ?", (new_ph_num, name))

        elif new_contant == 'other':
            new_other = input('tell me new other messages')
            self.c.execute("UPDATE CONTACT SET OTHER = ? WHERE NAME = ?", (new_other, name))

        else:
            print("? what did you say? I don't know")
            return 0

        self.conn.commit()
        print('info updated')


if __name__ == '__main__':
    contact = Contact()
    while True:
        start = "\n\
               \n1. add new Contact Person\
               \n2. search info\
               \n3. forget someone\
               \n4. update info\
               \n5. exit\n"

        print(start)
        choice = input('Your choice: ')
        if choice == '1':
            contact.add()

        elif choice == '2':
            contact.search()

        elif choice == '3':
            contact.delete()

        elif choice == '4':
            contact.update()

        elif choice == '5':
            contact.conn.close()
            print('Bye have a good time')
            sys.exit(0)

        else:
            print('What???')
