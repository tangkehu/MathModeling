list0 = [{'name':'a', 'num':1}, {'name':'b', 'num':2}, {'name':'a', 'num':3}, {'name':'a', 'num':5}]

list1 = [{'name':'a', 'num':1}, {'name':'b', 'num':2}, {'name':'a', 'num':3}, {'name':'a', 'num':5}]

for a in range(len(list0)):
    i = int()
    j = list()
    for b in range(len(list1)):
        if list0[a]['name'] == list1[b]['name']:
            i += list1[b]['num']
            j.append(b)
    for r in j:
        print r
        # list1.remove(list1[r])
    if i != list0[a]['num']:
        print i