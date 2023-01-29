"""
Work with Waifu API: download a new image(s) and open it, or open already existing ones.
"""
import WaifuAPI_conn
import WaifuAPI_db_com
import WaifuAPI_com_line
import argparse


parser = argparse.ArgumentParser(description='Get waifu image.')
parser.add_argument('-d', '--download', nargs='*', type=str, default='empty')
parser.add_argument('-o', '--open', nargs='*', type=str, default='empty')
args = vars(parser.parse_args())
download = args['download']
open_arg = args['open']


if download == 'empty' and open_arg == 'empty':
    while True:
        download_or_open = input("Would you like to download or open existing image?[D/o]")
        if any(a in download_or_open for a in ('D', 'd', 'Download', 'download')):
            image_json = WaifuAPI_conn.get_image()
            WaifuAPI_db_com.upload_to_db(image_json)
        elif any(a in download_or_open for a in ('O', 'o', 'Open', 'open')):
            WaifuAPI_conn.open_image()
        elif any(a in download_or_open for a in ('B', 'b', 'Break', 'break')):
            break
        else:
            print('Incorrect input. List of commands:')
            print('{} - {}'.format(('D', 'd', 'Download', 'download'), 'commands to download image(s)'))
            print('{} - {}'.format(('O', 'o', 'Open', 'open'), 'commands to open image(s)'))
            print('{} - {}'.format(('B', 'b', 'Break', 'break'), 'command for exit'))
else:
    WaifuAPI_com_line.command_line(download, open_arg)