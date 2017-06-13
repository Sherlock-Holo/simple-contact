#!/usr/bin/env python3

import os
import sqlite3

if os.path.exists('contact.db'):
    os.remove('contact.db')

conn = sqlite3.connect('contact.db')
c = conn.cursor()

c.execute('''CREATE TABLE CONTACT
            (NAME TEXT, PHONE_NUM TEXT, OTHER TEXT)''')

conn.commit()
conn.close()
