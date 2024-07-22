def removeSpaces(s_in: str) -> str:
    s = s_in
    while(len(s)>0 and s[0]==" "):
        s = s[1:]
    while(len(s)>0 and s[len(s)-1]==" "):
        s = s[:len(s)-1]
    return s
        

def read(direct = "settings.ini"):
    with open(direct) as f:
        data = dict()
        for line in f.readlines():
            if '=' not in line:
                continue
            line = line.replace('\n','')
            key, value = map(removeSpaces, line.split('='))
            data[key] = value
    f.close()
    return data

def save(data, direct = "settings.ini"):
    with open(direct, 'w') as f:
        for key in data:
            f.write(f"{key}={data[key]}\n")
    f.close()