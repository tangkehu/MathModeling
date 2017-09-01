list0 = [{'name':'a', 'num':1}, {'name':'b', 'num':2}, {'name':'a', 'num':3}, {'name':'a', 'num':5}, {'name':'b', 'num':2}]

flag = list()
for a in list0:
    if a['name'] in flag:
        continue
    else:
        i = int()
        for b in list0:
            if a['name'] == b['name']:
                i += b['num']
        if i != a['num']:
            print i
        flag.append(a['name'])