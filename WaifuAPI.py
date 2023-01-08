"""
Work with Waifu API: download a new image(s) and open it, or open already existing ones.
"""
import WaifuAPI_conn
import WaifuAPI_db_com

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