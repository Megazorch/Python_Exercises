file = input("Please enter path to file:")
with open(str(file), 'r', encoding='utf-8') as f:
    header = f.readline().split(',')
    while True:
        try:
            line = f.readline().split(',')
            if len(line) == 1:
                break
            for i in range(len(header)):
                print(header[i].strip() + ':' + line[i].strip(), end=' | ')
            print('\n')
        except:
            break
