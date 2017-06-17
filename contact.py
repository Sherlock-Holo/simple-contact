#!/usr/bin/env python3

import argparse
import sqlite3
import sys

# color
yellow = '\033[0;33m'
puple = '\033[0;35m'
backgroud = '\033[0m'
white = '\033[0;37m'

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
        query = ('%{}%'.format(query), '%{}%'.format(query), '%{}%'.format(query))

        result = []
        self.c.execute(
            "SELECT * FROM CONTACT WHERE NAME LIKE ? COLLATE NOCASE OR PHONE_NUM LIKE ? COLLATE NOCASE OR OTHER LIKE ? COLLATE NOCASE", query)

        for r in self.c.fetchall():
            if type(r) == tuple:
                result.append(r)

            else:
                continue

        if len(result) != 0:
            for contact in result:
                print(contant.format(*contact))

        else:
            print("{}There's nothing here{}".format(*info_color))

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

        if ask.lower() in ('yes', 'y'):
            self.c.execute("DELETE FROM CONTACT WHERE NAME = ?", (query,))
            self.conn.commit()
            print('{}You just have forgotten someone{}'.format(*info_color))

        elif ask.lower() in ('no', 'n'):
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

    def start_polling(self):
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
                self.add()

            elif choice == '2':
                self.search()

            elif choice == '3':
                self.delete()

            elif choice == '4':
                self.update()

            elif choice == '5':
                self.list()

            elif choice.lower() == 'e':
                self.conn.close()
                print('{}Bye~ Have a good time{}'.format(*info_color))
                sys.exit(0)

            else:
                print('\n\n{}? What do you want?{}'.format(*title_color))

# argparse
parser = argparse.ArgumentParser(description='a simple contact')
parser.add_argument('-f', '--dbfile', help='import your databse')

args = parser.parse_args()


if __name__ == '__main__':
    if args.dbfile:
        contact = Contact(args.dbfile)
        contact.start_polling()

    else:
        contact = Contact()
        contact.start_polling()
