import requests
import psycopg, os, re

from dotenv import load_dotenv
from psycopg.sql import SQL

load_dotenv()

def has_num_or_special(inputString):
    return bool(re.search(r'\d|\W', inputString))


while True:
    author = input('Enter author full name or last name:')
    if not has_num_or_special(author):
        break
    else:
        print('There should be no number or special marks. Please try again.')

#   ?q=j%20k%20rowling
author = author.split()
query_parameter = ''
for word in author:
    query_parameter += '%20' + word

url = 'https://openlibrary.org/search/authors.json?q='
headers = {'Accept': 'application/json'}
r = requests.get(url + query_parameter, headers=headers)

key = re.findall(r'"key": "(.+?)"', r.text)  # non-greedy mode
name = re.findall(r'"name": "(.+?)"', r.text)  # non-greedy mode

dict_of_authors = {}

for i in range(len(key)):
    dict_of_authors[i+1] = (key[i], name[i])

print("Total number of matches:", len(dict_of_authors))
for count in dict_of_authors:
    print(count, ' - ', dict_of_authors[count][1])

while True:
    choice = int(input('Please choose author by number:'))
    if choice <= len(dict_of_authors):  # !make check for negative numbers
        break
    else:
        print('You entered string or number bigger than the result. Please try again.')

url = 'https://openlibrary.org/authors/' + dict_of_authors[choice][0] + '/works.json'
headers = {'Accept': 'application/json'}
r = requests.get(url, headers=headers)

titles = re.findall(r'"title": "(.+?)"', r.text)  # non-greedy mode

dbname = os.getenv('DATABASE')
user = os.getenv('USER_OF_DB')
password = os.getenv('PASSWORD')
path_to_db = 'dbname=' + dbname + ' user=' + user + ' password=' + password +' host=localhost'

with psycopg.connect(path_to_db) as conn:

    # Open a cursor to perform database operations
    with conn.cursor() as cur:

        # Execute a command: this creates a new table
        try:
            cur.execute("""
                        CREATE TABLE authors (
                            id_author BIGSERIAL NOT NULL PRIMARY KEY,
                            key VARCHAR(15) NOT NULL,
                            name VARCHAR(50) NOT NULL,
                            UNIQUE(key))
                        """)    # add UNIQUE(key) after successful test

            cur.execute("""
                        CREATE TABLE books (
                            id_book BIGSERIAL NOT NULL PRIMARY KEY,
                            title VARCHAR(200) NOT NULL,
                            author BIGINT REFERENCES authors (id_author))
                        """)    # UNIQUE(title))
                                # I found duplicates of titles, fuck them, I am tired.
        except psycopg.errors.DuplicateTable:
            print("Table(s) already exists.")
            conn.rollback()

        cur.execute("INSERT INTO authors (key, name) VALUES (%s, %s)",
                        (dict_of_authors[choice][0], dict_of_authors[choice][1]))

        for book_title in titles:
            cur.execute("INSERT INTO books (title) VALUES (%s)", [book_title])  # there are always should be a sequence
                                                                                # MaZa FaKa !

        cur.execute("SELECT id_author FROM authors WHERE name = %s", [dict_of_authors[choice][1]])
        db_id_author = cur.fetchone()[0]  # bitch returns (1, ) WHY?
        books_to_update = []
        for book_title in titles:
            cur.execute("SELECT id_book FROM books WHERE title = %s", [book_title])
            books_to_update.append(cur.fetchone()[0])

        for id_num in books_to_update:
            cur.execute(SQL("UPDATE books SET author = {} WHERE id_book = {}").format(db_id_author, id_num))

        conn.commit()