import psycopg, os, requests
import webbrowser

from dotenv import load_dotenv
from copy import deepcopy
load_dotenv()

url = "https://api.waifu.im/search/?"

versatile = ['maid', 'waifu', 'marin-kitagawa', 'mori-calliope',
             'raiden-shogun', 'oppai', 'selfies', 'uniform']

nsfw = ['ass', 'hentai', 'milf', 'oral', 'paizuri', 'ecchi', 'ero']

list_of_tags = "{:<1} - {:>2}"

#included_tags = ''
# excluded_tags = ''
is_nsfw = ''
# gif = ''
many = ''

def gather_tags(ver_tags=[], nsfw_tags=[], ver_list=[], nsfw_list=[]):
    tags = ''
    if ver_tags == '' and len(nsfw_tags) > 0:
        for num in nsfw_tags:
            tags += "&included_tags={}".format(nsfw_list[int(num.strip()) - 1])
        return tags
    elif len(ver_tags) > 0 and nsfw_tags == '':
        for num in ver_tags:
            tags += "&included_tags={}".format(ver_list[int(num.strip()) - 1])
        return tags
    elif ver_tags == '' and nsfw_tags == '':
        return tags
    else:
        for num in ver_tags:
            tags += "&included_tags={}".format(ver_list[int(num.strip()) - 1])
        for num in nsfw_tags:
            tags += "&included_tags={}".format(nsfw_list[int(num.strip()) - 1])
        return tags

while True:
    random_search_y_n = input('Random search?[Y/n]')
    if any(a in random_search_y_n for a in ('Y', 'y', 'Yes', 'yes')):
        one_or_many = input('One or many?[1/m]')
        if any(a in one_or_many for a in ('1', 'one')):
            included_tags = gather_tags()   # should return empty str
            many = '&many=false'
            break
        elif any(a in one_or_many for a in ('M', 'm', 'Many', 'many')):
            included_tags = gather_tags()  # should return empty str
            many = '&many=true'
            break
        else:
            print('Input', one_or_many, 'is incorrect. Please try again.')
    elif any(a in random_search_y_n for a in ('N', 'n', 'No', 'no')):
        print('Versatile tags:')
        for tag_num in range(len(versatile)):
            print(list_of_tags.format(tag_num + 1, versatile[tag_num]))
        chosen_ver_tags = input('Choose tags by numbers (1,2,10):')
        chosen_ver_tags = chosen_ver_tags.split(',')

        nsfw_y_n = input("Include NSFW (not safe/suitable for work) tags?[Y/n]")
        if any(a in nsfw_y_n for a in ('Y', 'y', 'Yes', 'yes')):
            nsfw_random = input('Random or force include?[R/f]')
            if any(a in nsfw_random for a in ('R', 'r', 'Random', 'random')):
                is_nsfw = '&is_nsfw=true'
                chosen_nsfw_tags = ''
            elif any(a in nsfw_random for a in ('F', 'f', 'Force', 'force')):
                print('NSFW tags:')
                for tag_num in range(len(nsfw)):
                    print(list_of_tags.format(tag_num + 1, nsfw[tag_num]))
                chosen_nsfw_tags = input('Choose tags by numbers (1,2,10):')
                chosen_nsfw_tags = chosen_nsfw_tags.split(',')
                is_nsfw = ''
            else:
                print('Error. NSFW set to False.')
                chosen_nsfw_tags = ''
                is_nsfw = '&is_nsfw=false'
        elif any(a in nsfw_y_n for a in ('N', 'n', 'No', 'no')):
            chosen_nsfw_tags = ''
            is_nsfw = '&is_nsfw=false'
        else:
            print('Input', nsfw_y_n, 'is incorrect. NSFW is set to False.')
            chosen_nsfw_tags = ''
            is_nsfw = '&is_nsfw=false'

        one_or_many = input('One or many?[1/m]')
        if any(a in one_or_many for a in ('1', 'one')):
            included_tags = gather_tags(chosen_ver_tags, chosen_nsfw_tags, versatile, nsfw)
            many = '&many=false'
            break
        elif any(a in one_or_many for a in ('M', 'm', 'Many', 'many')):
            included_tags = gather_tags(chosen_ver_tags, chosen_nsfw_tags, versatile, nsfw)
            many = '&many=true'
            break
        else:
            print('Input', one_or_many, 'is incorrect. Many set to False.')
            many = '&many=false'
    else:
        print('Your input is incorrect. Please try again.')

full_url = url + included_tags + is_nsfw + many
print(full_url)
r = requests.get(full_url)

r = r.json()

dbname = os.getenv('DATABASE')
user = os.getenv('USER_OF_DB')
password = os.getenv('PASSWORD')
path_to_db = 'dbname=' + dbname + ' user=' + user + ' password=' + password +' host=localhost'

with psycopg.connect(path_to_db) as conn:

    with conn.cursor() as cur:

        try:
            cur.execute("""
                        CREATE TABLE images (
                            signature VARCHAR(20) NOT NULL,
                            extension VARCHAR(6) NOT NULL,
                            image_id INTEGER NOT NULL,
                            favourites INTEGER NOT NULL,
                            dominant_color VARCHAR(10) NOT NULL,
                            source VARCHAR(80) NOT NULL,
                            uploaded_at DATE NOT NULL,
                            liked_at VARCHAR(10),
                            is_nsfw BOOLEAN NOT NULL,
                            width INTEGER NOT NULL,
                            height INTEGER NOT NULL,
                            url VARCHAR(50) NOT NULL,
                            preview_url VARCHAR(60) NOT NULL,
                            seen INTEGER,
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
            print("Table(s) is/are already existed.")
            conn.rollback()

        for i in range(len(r['images'])):
            image_dict = deepcopy(r['images'][i])
            image_dict.pop('tags')
            image_values = list(image_dict.values())

            image_tags = (r['images'][i]['tags'][0]).values()
            # I tried to use JSON adaptation via 'from psycopg.types.json import Jsonb'
            # but it seems impossible for me to implement this feature for big number
            # of columns. (Someone is silently crying.)
            try:
                cur.execute("""INSERT INTO images VALUES (%s,%s,%s,%s,%s,
                                %s,%s,%s,%s,%s,%s,%s,%s)""", image_values)

                cur.execute("""INSERT INTO tags (tag_id, name, description, is_nsfw)
                                VALUES (%s,%s,%s,%s)""", list(image_tags))
            except psycopg.errors.UniqueViolation:
                print('Image',image_values[0], 'is in the base.')
                conn.rollback()

            cur.execute("SELECT image_id FROM images WHERE signature = %s", [image_values[0]])
            db_image_id = cur.fetchone()[0]

            cur.execute("UPDATE tags SET image_id = (%s) WHERE image_id IS NULL", [db_image_id])

            cur.execute('SELECT * FROM images JOIN tags ON images.image_id = tags.image_id')

        image_to_see = input('Which image do you want to see: already seen, not seen yet or all?[seen, not, all]')
        print(image_to_see)
        if any(a in image_to_see for a in ('Seen', 'seen', 'S', 's')):
            cur.execute("SELECT url, seen FROM images WHERE seen >= 1")
            image_urls = cur.fetchall()
            for image_url in range(len(image_urls)):
                print('url -', image_urls[image_url][0], 'seen -', image_urls[image_url][1])
                webbrowser.open(image_urls[image_url][0])
            cur.execute("UPDATE images SET seen = seen + 1 WHERE seen >= 1")
        elif any(a in image_to_see for a in ('Not', 'not', 'N', 'n')):
            cur.execute("SELECT url, seen FROM images WHERE seen IS NULL")
            image_urls = cur.fetchall()
            for image_url in range(len(image_urls)):
                print('url -', image_urls[image_url][0], 'seen -', image_urls[image_url][1])
                webbrowser.open(image_urls[image_url][0])
            cur.execute("UPDATE images SET seen = 1 WHERE seen IS NULL")
        elif any(a in image_to_see for a in ('All', 'all', 'a', 'ALL')):
            cur.execute("SELECT url, seen FROM images")
            image_urls = cur.fetchall()
            for image_url in range(len(image_urls)):
                print('url -', image_urls[image_url][0], 'seen -', image_urls[image_url][1])
                webbrowser.open(image_urls[image_url][0])
            cur.execute("UPDATE images SET seen = seen + 1 WHERE seen >= 1")
            cur.execute("UPDATE images SET seen = 1 WHERE seen IS NULL")
        else:
            print(image_to_see, "is incorrect input. You'll see nothing.")

        conn.commit()
