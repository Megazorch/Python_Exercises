"""
Store all commands for database.
"""
import psycopg
import os
import webbrowser
from dotenv import load_dotenv
from copy import deepcopy

load_dotenv()


def connect_to_db():
    """
    Set connection to database.
    return psycopg.connect(path_to_db):
    """
    dbname = os.getenv('DATABASE')
    user = os.getenv('USER_OF_DB')
    password = os.getenv('PASSWORD')
    path_to_db = 'dbname=' + dbname + ' user=' + user + ' password=' + password + ' host=localhost'

    return psycopg.connect(path_to_db)


def create_tables(connection):
    """
    Create tables to store image data.
    :return:
    """

    with connection.cursor() as cur:
        try:
            cur.execute("""
                        CREATE TABLE images (
                            signature VARCHAR(20) NOT NULL,
                            extension VARCHAR(6) NOT NULL,
                            image_id INTEGER NOT NULL,
                            favourites INTEGER NOT NULL,
                            dominant_color VARCHAR(10) NOT NULL,
                            source VARCHAR(80),
                            uploaded_at DATE NOT NULL,
                            liked_at VARCHAR(10),
                            is_nsfw BOOLEAN NOT NULL,
                            width INTEGER NOT NULL,
                            height INTEGER NOT NULL,
                            url VARCHAR(50) NOT NULL,
                            preview_url VARCHAR(60) NOT NULL,
                            seen INTEGER,
                            new BOOLEAN,
                            UNIQUE(signature),
                            UNIQUE(image_id))
                        """)

            cur.execute("""
                        CREATE TABLE tags (
                            id_tag BIGSERIAL NOT NULL PRIMARY KEY,
                            tag_id INTEGER NOT NULL,
                            name VARCHAR(15) NOT NULL,
                            description TEXT,
                            is_nsfw BOOLEAN NOT NULL,
                            image_id INTEGER REFERENCES images (image_id))
                        """)
        except psycopg.errors.DuplicateTable:
            print("Tables are already existed.")
            connection.rollback()

        connection.commit()


def upload_to_db(image_json):
    """
    Upload image data to database.
    :param image_json:
    :return:
    """
    connection = connect_to_db()

    with connection.cursor() as cur:
        cur.execute("""SELECT EXISTS ( SELECT FROM pg_tables
                        WHERE schemaname = 'public' AND tablename  = 'images' )""")
        if not cur.fetchone()[0]:
            create_tables(connection)

        for idx, value in enumerate(image_json['images']):
            image_dict = deepcopy(value)
            image_dict.pop('tags')
            image_values = list(image_dict.values())

            image_tags = (image_json['images'][idx]['tags'][0]).values()
            # I tried to use JSON adaptation via 'from psycopg.types.json import Jsonb'
            # but it seems impossible for me to implement this feature for big number
            # of columns. (Someone is silently crying.)
            try:
                cur.execute("""INSERT INTO images VALUES (%s,%s,%s,%s,%s,
                                %s,%s,%s,%s,%s,%s,%s,%s)""", image_values)

                cur.execute("""INSERT INTO tags (tag_id, name, description, is_nsfw)
                                VALUES (%s,%s,%s,%s)""", list(image_tags))
            except psycopg.errors.UniqueViolation:
                connection.rollback()
                print('Image', image_values[0], 'is in the base.')

            cur.execute("SELECT image_id FROM images WHERE signature = %s", [image_values[0]])
            db_image_id = cur.fetchone()[0]

            cur.execute("UPDATE tags SET image_id = (%s) WHERE image_id IS NULL", [db_image_id])
            cur.execute("UPDATE images SET new = True WHERE new IS NULL")

        connection.commit()
        return print('Image uploaded to database.')
        # cur.execute('SELECT * FROM images JOIN tags ON images.image_id = tags.image_id')


def open_seen_image():
    """
    Open all seen images in web browser.
    :return:
    """
    connection = connect_to_db()

    with connection.cursor() as cur:
        cur.execute("SELECT url, seen FROM images WHERE seen >= 1")
        image_urls = cur.fetchall()
        for idx, image_url in enumerate(image_urls):
            print('url -', image_url[0], 'seen -', image_url[1])
            webbrowser.open(image_url[0])
        cur.execute("UPDATE images SET seen = seen + 1 WHERE seen >= 1")

        connection.commit()


def open_not_seen_images():
    """
    Open all not seen images in web browser.
    :return:
    """
    connection = connect_to_db()

    with connection.cursor() as cur:
        cur.execute("SELECT url, seen FROM images WHERE seen IS NULL")
        image_urls = cur.fetchall()
        for idx, image_url in enumerate(image_urls):
            print('url -', image_url[0], 'seen -', image_url[1])
            webbrowser.open(image_url[0])
        cur.execute("UPDATE images SET seen = 1 WHERE seen IS NULL")

        connection.commit()


def open_all_images():
    """
    Open all images in web browser.
    :return:
    """
    connection = connect_to_db()

    with connection.cursor() as cur:
        cur.execute("SELECT url, seen FROM images")
        image_urls = cur.fetchall()
        for idx, image_url in enumerate(image_urls):
            print('url -', image_url[0], 'seen -', image_url[1])
            webbrowser.open(image_url[0])
        cur.execute("UPDATE images SET seen = seen + 1 WHERE seen >= 1")
        cur.execute("UPDATE images SET seen = 1 WHERE seen IS NULL")

        connection.commit()


def open_new():
    """
    Open a new image(s) in web browser.
    :return:
    """
    connection = connect_to_db()

    with connection.cursor() as cur:
        cur.execute("SELECT url, seen FROM images WHERE new IS TRUE")
        image_urls = cur.fetchall()
        for idx, image_url in enumerate(image_urls):
            print('url -', image_url[0], 'seen -', image_url[1])
            webbrowser.open(image_url[0])
        cur.execute("UPDATE images SET new = False WHERE new IS TRUE")
        cur.execute("UPDATE images SET seen = 1 WHERE seen IS NULL")

        connection.commit()
