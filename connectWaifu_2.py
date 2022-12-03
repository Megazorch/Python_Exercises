from urllib.request import urlopen
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://api.waifu.im/search/?"

html = urlopen(url, context=ctx).read()
data = html.decode()
js = json.loads(data)

step = 1

with open('waifu.csv', mode='r+', encoding='utf-8') as csvfile:
    junkObj = csvfile.readlines()
    if len(junkObj) == 0:
        count2 = 0
    else:
        count2 = len(junkObj)
    print(len(junkObj))
    stop = 0
    while stop < 1:
        if count2 == 0:
            for x, y in js['images'][0].items():
                if '"' in x:
                    if step == len(js['images'][0]):
                        csvfile.write('""' + x + '""\n')
                    else:
                        csvfile.write('""' + x + '"", ')
                        step = step + 1
                if ',' in x:
                    if step == len(js['images'][0]):
                        csvfile.write('"' + x + '"\n')
                    else:
                        csvfile.write('"' + x + '", ')
                        step = step + 1
                if step == len(js['images'][0]):
                    csvfile.write(x + '\n')  # header
                else:
                    csvfile.write(x + ', ')
                    step = step + 1
            step = 0
            count2 = count2 + 1
        else:
            for x, y in js['images'][0].items():
                if len(str(y)) > 80:
                    y = str(y)[:80]

                if '"' in str(y):
                    if step == len(js['images'][0]):
                        csvfile.write('""' + str(y) + '""\n')
                        break
                    else:
                        csvfile.write('""' + str(y) + '"", ')
                        step = step + 1
                if ',' in str(y):
                    if step == len(js['images'][0]):
                        csvfile.write('"' + str(y) + '"\n')
                        break
                    else:
                        csvfile.write('"' + str(y) + '", ')
                        step = step + 1
                if step == len(js['images'][0]):
                    csvfile.write(str(y) + '\n')  # header
                    break
                else:
                    csvfile.write(str(y) + ', ')
                    step = step + 1

            stop = stop + 1
