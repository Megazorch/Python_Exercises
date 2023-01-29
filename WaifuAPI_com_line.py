import requests
import WaifuAPI_db_com

versatile = ['maid', 'waifu', 'marin-kitagawa', 'mori-calliope',
             'raiden-shogun', 'oppai', 'selfies', 'uniform']

nsfw = ['ass', 'hentai', 'milf', 'oral', 'paizuri', 'ecchi', 'ero']

included_tags = []


def get_image(included_tags=None, is_nsfw=None, many='false'):
    """
    Download image.
    :return r.json():
    """
    url = "https://api.waifu.im/search/?"
    tags = {'included_tags': included_tags, 'is_nsfw': is_nsfw, 'many': many}
    r = requests.get(url, params=tags)

    return r.json()


def command_line(download, open_arg):
    """
    Receive arguments from terminal. Can download or open images.
    :param download:
    :param open_arg:
    :return:
    """
    if True is isinstance(download, list) and open_arg == 'empty':

        if download[0] == 'random':
            if download[1] == 'one':
                get_image()
            elif download[1] == 'many':
                get_image(many='true')
            else:
                print("Incorrect input. Expecting something like: 'random one' or 'random many'.")
        elif download[0] == 'force':
            try:
                chosen_ver_tags = download[1].split(',')
                for num in chosen_ver_tags:
                    included_tags.append(versatile[int(num.strip()) - 1])
                print(included_tags)
            except ValueError:
                print("Incorrect input. Expecting: 'force 1,2,3'")
                exit()
            except IndexError:
                print("Incorrect input. Expecting: 'force 1,2,3'")
                exit()

            try:
                if download[2] == 'nsfw-random':
                    is_nsfw = 'true'
                    try:
                        if download[3] == 'many':
                            many = 'true'
                    except IndexError:
                        many = 'false'
                elif download[2] == 'nsfw-force':
                    try:
                        chosen_nsfw_tags = download[3].split(',')
                        for num in chosen_nsfw_tags:
                            included_tags.append(nsfw[int(num.strip()) - 1])
                        print(included_tags)
                        is_nsfw = None
                    except ValueError:
                        print("Incorrect input. Expecting: 'nsfw-force 1,2,3'")
                        exit()
                    except IndexError:
                        print("Incorrect input. Expecting: 'nsfw-force 1,7' (not more than 7 or less than -6)")
                        exit()

                    try:
                        if download[4] == 'many':
                            many = 'true'
                    except (ValueError, IndexError):
                        many = 'false'

                elif download[2] == 'nsfw-true':
                    is_nsfw = 'true'
                    try:
                        if download[3] == 'many':
                            many = 'true'
                    except (ValueError, IndexError):
                        many = 'false'
                elif download[2] == 'many':
                    is_nsfw = 'false'
                    many = 'true'
                else:
                    print("Incorrect input. Expecting: 'nsfw-random', 'nsfw-force', 'nsfw-true' or 'many'")
                    exit()
            except IndexError:
                is_nsfw = 'false'
                many = 'false'
        else:
            print("Incorrect input. Try -h for help.")

        image_json = get_image(included_tags, is_nsfw, many)
        WaifuAPI_db_com.upload_to_db(image_json)

    elif True is isinstance(open_arg, list) and download == 'empty':
        try:
            if open_arg[0] == 'seen':
                WaifuAPI_db_com.open_seen_image()
            elif open_arg[0] == 'not-seen':
                WaifuAPI_db_com.open_not_seen_images()
            elif open_arg[0] == 'all':
                WaifuAPI_db_com.open_all_images()
            elif open_arg[0] == 'new':
                WaifuAPI_db_com.open_new()
            else:
                print(open_arg[0], 'is incorrect input. Try: seen, not-seen, new or all.')
        except IndexError:
            print('Incorrect input. Expecting: -o seen; -o not-seen; -o all; -o new.')
