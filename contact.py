#!/usr/bin/env python3

import sqlite3
import sys

# color
yellow = '\033[0;33m'
puple = '\033[0;35m'
backgroud = '\033[0m'

contant = "\n\033[0;35mname\033[0m: \033[0;33m{}\033[0m\
           \n\033[0;35mphone number\033[0m: \033[0;33m{}\033[0m\
           \n\033[0;35mother\033[0m: \033[0;33m{}\033[0m\n"


class Contact:
    def __init__(self, db='contact.db'):
        self.db = db
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()

    def add(self):
        name = input('Please input name: ')
        phone_num = input('Please input phone_num: ')
        other = input('Other messages?(optional) ')
        print('\n\n')

        contant = (name, phone_num, other)
        self.c.execute("INSERT INTO CONTACT VALUES(?, ?, ?)", contant)
        self.conn.commit()

        print('info added')

    def search(self):
        query = input('What do you want to search? ')
        print('\n\n')
        query = (query, query, query)
        self.c.execute("SELECT * FROM CONTACT WHERE NAME = ? OR PHONE_NUM = ? OR OTHER = ?", query)
        result = self.c.fetchone()

        if type(result) == tuple:
            print(contant.format(*result))

        else:
            print('Sorry~ No result')


    def delete(self):
        query = input('Who do you want to forget? ')

        self.c.execute("SELECT * FROM CONTACT WHERE NAME = ?", (query,))
        result = self.c.fetchone()
        if type(result) == tuple:
            print(contant.format(*result))

        else:
            print('Sorry~ No result')

        ask = input("Do you want to forget him/her? tell me (yes) or (no)")
        print('\n\n')
        if ask.lower() == 'yes':
            self.c.execute("DELETE FROM CONTACT WHERE NAME = ?", (query,))
            self.conn.commit()
            print('You just have forgotten someone')

        elif ask.lower() == 'no':
            print("You still can't forget him/her, right?")

    def update(self):
        name = input('You have new info about who? ')
        self.c.execute("SELECT * FROM CONTACT WHERE NAME = ?", (name,))
        result = self.c.fetchone()
        if type(result) == tuple:
            print(contant.format(*result))

            new_contant = input('What do you want to update, name, phone or other? ')

            if new_contant == 'name':
                new_name = input('tell me new name ')
                self.c.execute("UPDATE CONTACT SET NAME = ? WHERE NAME = ?",
                               (new_name, name))

            elif new_contant == 'phone':
                new_ph_num = input('tell me new phone number: ')
                self.c.execute("UPDATE CONTACT SET PHONE_NUM = ? WHERE NAME = ?",
                               (new_ph_num, name))

            elif new_contant == 'other':
                new_other = input('tell me new other messages')
                self.c.execute("UPDATE CONTACT SET OTHER = ? WHERE NAME = ?",
                               (new_other, name))

            else:
                print("? what did you say? I don't know")
                return 0

            self.conn.commit()
            print('\n\n')
            print('info updated')

        else:
            print('ah? Who did you say?')
            return 0



    def list(self):
        self.c.execute("SELECT * FROM CONTACT")
        for p in self.c.fetchall():
            print(contant.format(*p))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == ('-h' or '--help'):
            # debug
            print(sys.argv[1])

            print('contact.py [db file]\
                 \nTips: If you run contact.py first time, please run db_init.py at first\
                 \n        -h --help    show this help and exit\
                 \n        [db file]    use your database')

            sys.exit(0)

        else:
            contact = Contact(sys.argv[1])

    elif len(sys.argv) == 1:
        contact = Contact()

    else:
        sys.exit(1)


    while True:
        start = "\n\
               \n1. add new Contact Person\
               \n2. search info\
               \n3. forget someone\
               \n4. update info\
               \n5. list all contacts\
               \n6. exit\n"

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
            contact.list()

        elif choice == '6':
            contact.conn.close()
            print('Bye have a good time')
            sys.exit(0)

        else:
            print('\n\nWhat???')
