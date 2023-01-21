"""
Connect to Waifu API, get json file with data, add this data to database
and then open image in web browser.
"""
import requests
import WaifuAPI_db_com


def get_image():
    """
    Gather tags, connect to API and return json object with image data.
    """
    versatile = ['maid', 'waifu', 'marin-kitagawa', 'mori-calliope',
                 'raiden-shogun', 'oppai', 'selfies', 'uniform']

    nsfw = ['ass', 'hentai', 'milf', 'oral', 'paizuri', 'ecchi', 'ero']

    list_of_tags = "{:<1} - {:>2}"

    included_tags = []
    # excluded_tags = ''
    # gif = ''

    while True:
        random_search_y_n = input('Random search?[Y/n]')
        if any(a in random_search_y_n for a in ('Y', 'y', 'Yes', 'yes')):
            one_or_many = input('One or many?[1/m]')
            if any(a in one_or_many for a in ('1', 'one')):
                included_tags = None
                is_nsfw = None
                many = 'false'
                break
            elif any(a in one_or_many for a in ('M', 'm', 'Many', 'many')):
                included_tags = None
                is_nsfw = None
                many = 'true'
                break
            else:
                print('Input', one_or_many, 'is incorrect. Please try again.')
        elif any(a in random_search_y_n for a in ('N', 'n', 'No', 'no')):
            print('Versatile tags:')
            for tag_num, tag_value in enumerate(versatile, start=1):
                print(list_of_tags.format(tag_num, tag_value))
            chosen_ver_tags = input('Choose tags by numbers (1,2,10):')
            chosen_ver_tags = chosen_ver_tags.split(',')
            for num in chosen_ver_tags:
                included_tags.append(versatile[int(num.strip()) - 1])

            nsfw_y_n = input("Include NSFW (not safe/suitable for work) tags?[Y/n]")
            if any(a in nsfw_y_n for a in ('Y', 'y', 'Yes', 'yes')):
                nsfw_random = input('Random or force include?[R/f]')
                if any(a in nsfw_random for a in ('R', 'r', 'Random', 'random')):
                    is_nsfw = 'true'
                elif any(a in nsfw_random for a in ('F', 'f', 'Force', 'force')):
                    print('NSFW tags:')
                    for tag_num, tag_value in enumerate(nsfw, start=1):
                        print(list_of_tags.format(tag_num, tag_value))
                    chosen_nsfw_tags = input('Choose tags by numbers (1,2,10):')
                    chosen_nsfw_tags = chosen_nsfw_tags.split(',')
                    for num in chosen_nsfw_tags:
                        included_tags.append(nsfw[int(num.strip()) - 1])
                    is_nsfw = None  # should not be added
                else:
                    print('Error. NSFW set to False.')
                    is_nsfw = 'false'
            elif any(a in nsfw_y_n for a in ('N', 'n', 'No', 'no')):
                is_nsfw = 'false'
            else:
                print('Input', nsfw_y_n, 'is incorrect. NSFW is set to False.')
                is_nsfw = 'false'

            one_or_many = input('One or many?[1/m]')
            if any(a in one_or_many for a in ('1', 'one')):
                many = 'false'
                break
            elif any(a in one_or_many for a in ('M', 'm', 'Many', 'many')):
                many = 'true'
                break
            else:
                print('Input', one_or_many, 'is incorrect. Many set to False.')
                many = 'false'
                break
        else:
            print('Your input is incorrect. Please try again.')

    url = "https://api.waifu.im/search/?"
    tags = {'included_tags': included_tags, 'is_nsfw': is_nsfw, 'many': many}
    r = requests.get(url, params=tags)

    return r.json()


def open_image():
    """
    Choose which image to open.
    :return:
    """
    while True:
        image_to_see = input('Which image do you want to see: seen, not seen, all or new?[seen, not or nt, all, new]')
        if any(a in image_to_see for a in ('Seen', 'seen', 'S', 's')):
            WaifuAPI_db_com.open_seen_image()
            break
        elif any(a in image_to_see for a in ('Not', 'not', 'NT', 'nt')):
            WaifuAPI_db_com.open_not_seen_images()
            break
        elif any(a in image_to_see for a in ('All', 'all', 'a', 'ALL')):
            WaifuAPI_db_com.open_all_images()
            break
        elif any(a in image_to_see for a in ('New', 'new', 'n', 'N')):
            WaifuAPI_db_com.open_new()
            break
        else:
            print(image_to_see, "is incorrect input. Please try again. List of commands:")
            print('{} - {}'.format(('Seen', 'seen', 'S', 's'), 'commands to open seen image(s)'))
            print('{} - {}'.format(('Not', 'not', 'NT', 'nt'), 'commands to open not seen image(s)'))
            print('{} - {}'.format(('All', 'all', 'a', 'ALL'), 'commands to open all images'))
            print('{} - {}'.format(('New', 'new', 'n', 'N'), 'commands to open a new image(s)'))
