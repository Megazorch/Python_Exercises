from urllib.request import urlopen
import json
import ssl
import csv
import sqlite3

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#creat_url = input

url = "https://api.waifu.im/random/?"


html = urlopen(url, context=ctx).read()
data = html.decode()
js = json.loads(data)

with open('waifu.csv', 'a') as csvfile:
    fieldnames = ['query', 'value']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for x, y in js['images'][0].items():
        if x == 'tags':
            for i in range(len(js['images'][0]['tags'])):
                for key, value in js['images'][0]['tags'][i].items():
                    writer.writerow({'query': key, 'value': value})
        else:
            writer.writerow({'query': x, 'value': y})


with open('waifu.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['query'], row['value'])

#print(js['images'][0]['url'])
#print(len(js['images'][0]))
#for i in range(len(js['images'][0])):

#print(json.dumps(js, indent=3))
