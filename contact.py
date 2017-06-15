#!/usr/bin/env python3

import argparse
import sqlite3
import sys

# color
yellow = '\033[0;33m'
puple = '\033[0;35m'
backgroud = '\033[0m'

title_color = (puple, backgroud)
info_color = (yellow, backgroud)

contant = "\n\033[0;35mname\033[0m: \033[0;33m{}\033[0m\
           \n\033[0;35mphone number\033[0m: \033[0;33m{}\033[0m\
           \n\033[0;35mother\033[0m: \033[0;33m{}\033[0m\n"


class Contact:

    def __init__(self, db='contact.db'):
        self.db = db
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()

    def add(self):
        name = input('{}Please input name:{} '.format(*title_color))
        phone_num = input('{}Please input phone_num:{} '.format(*title_color))
        other = input('{}Other messages?(optional){} '.format(*title_color))

        if name == '' or phone_num == '':
            print('\n\n{}At least you should tell me require info{}'.format(*info_color))
            return 0

        else:
            print('\n\n')

            contant = (name, phone_num, other)
            self.c.execute("INSERT INTO CONTACT VALUES(?, ?, ?)", contant)
            self.conn.commit()

            print('{}contact added{}'.format(*info_color))

    def search(self):
        query = input('{}What do you want to search?{} '.format(*title_color))
        print('\n\n')
        query = (query, query, query)
        self.c.execute(
            "SELECT * FROM CONTACT WHERE NAME = ? COLLATE NOCASE OR PHONE_NUM = ? COLLATE NOCASE OR OTHER = ? COLLATE NOCASE", query)
        result = self.c.fetchone()

        if type(result) == tuple:
            print(contant.format(*result))

        else:
            print('{}Sorry~ No result{}'.format(*info_color))

    def delete(self):
        query = input('{}Who do you want to forget?{} '.format(*title_color))

        self.c.execute("SELECT * FROM CONTACT WHERE NAME = ? COLLATE NOCASE", (query,))
        result = self.c.fetchone()
        if type(result) == tuple:
            print(contant.format(*result))

        else:
            print('{}Sorry~ No result{}'.format(*info_color))

        ask = input("{}Do you want to forget him/her? tell me (Y)es or (N)o:{} ".format(*title_color))
        print('\n\n')

        if ask.lower() == ('yes' or 'y'):
            self.c.execute("DELETE FROM CONTACT WHERE NAME = ?", (query,))
            self.conn.commit()
            print('{}You just have forgotten someone{}'.format(*info_color))

        elif ask.lower() == ('no' or 'n'):
            print("{}You still can't forget him/her, right?{}".format(*info_color))

    def update(self):
        name = input('{}You have new info about who?{} '.format(title_color))
        self.c.execute("SELECT * FROM CONTACT WHERE NAME = ?", (name,))
        result = self.c.fetchone()
        if type(result) == tuple:
            print(contant.format(*result))

            new_contant = input(
                '{}What do you want to update, name, phone or other?{} '.format(title_color))

            if new_contant == 'name':
                new_name = input('{}tell me new name:{} '.format(title_color))
                if new_name:
                    self.c.execute("UPDATE CONTACT SET NAME = ? WHERE NAME = ?",
                                   (new_name, name))

                else:
                    print("{}You haven't change anything{}".format(*info_color))

            elif new_contant == 'phone':
                new_ph_num = input('{}tell me new phone number:{} '.format(title_color))
                if new_ph_num:
                    self.c.execute("UPDATE CONTACT SET PHONE_NUM = ? WHERE NAME = ?",
                                   (new_ph_num, name))

                else:
                    print("{}You haven't change anything{}".format(*info_color))

            elif new_contant == 'other':
                new_other = input('{}tell me new other messages:{} '.format(title_color))
                if new_other:
                    self.c.execute("UPDATE CONTACT SET OTHER = ? WHERE NAME = ?",
                                   (new_other, name))

                else:
                    print("{}You haven't change anything{}".format(*info_color))

            else:
                print("{}? what did you say? I don't know{}".format(title_color))
                return 0

            self.conn.commit()
            print('\n\n')
            print('{}info updated{}'.format(info_color))

        else:
            print('{}ah? Who did you say?{}'.format(title_color))
            return 0

    def list(self):
        self.c.execute("SELECT * FROM CONTACT")
        for p in self.c.fetchall():
            print(contant.format(*p))


# argparse
parser = argparse.ArgumentParser(description='a simple contact')
parser.add_argument('-f', '--dbfile', help='import your databse')


args = parser.parse_args()

# main
def main(*dbfile):
    if len(dbfile) == 0:
        contact = Contact()

    else:
        contact = Contact(dbfile[0])
    while True:

        start = "{}\n\
               \n1. add new Contact Person\
               \n2. search info\
               \n3. forget someone\
               \n4. update info\
               \n5. list all contacts\
               \ne. exit\n{}".format(*title_color)

        print(start)
        choice = input('{}Your choice:{} '.format(*info_color))
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

        elif choice.lower() == 'e':
            contact.conn.close()
            print('{}Bye~ Have a good time{}'.format(*info_color))
            sys.exit(0)

        else:
            print('\n\n{}? What do you want?{}'.format(*title_color))

if args.dbfile:
    main(args.dbfile)

else:
    main()
