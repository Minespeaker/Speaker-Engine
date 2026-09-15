def inrange(l, t, h, iseq=True):
    if iseq:
        out = l <= t <= h
    else:
        out = l < t < h
        
    return out

def sort(list, list2):
    list3 = []
    for i in range (len(list2)):
        list3.append(list2.index(min(list2)))
        list2[list3[-1]] = 99999999999
    list4 = [list[list3[i]] for i in range (len(list))]
    return(list4)