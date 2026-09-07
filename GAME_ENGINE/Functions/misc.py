
def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    diff = mx - mn

    # Hue
    if diff == 0:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    else:
        h = (60 * ((r - g) / diff) + 240) % 360

    # Saturation
    s = 0 if mx == 0 else diff / mx

    # Value
    v = mx

    return h, s, v

def hsv_to_rgb(h, s, v):
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if 0 <= h < 60:
        rp, gp, bp = c, x, 0
    elif 60 <= h < 120:
        rp, gp, bp = x, c, 0
    elif 120 <= h < 180:
        rp, gp, bp = 0, c, x
    elif 180 <= h < 240:
        rp, gp, bp = 0, x, c
    elif 240 <= h < 300:
        rp, gp, bp = x, 0, c
    else:
        rp, gp, bp = c, 0, x

    r = int((rp + m) * 255)
    g = int((gp + m) * 255)
    b = int((bp + m) * 255)

    return r, g, b

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

def alph_list(data_list):
  """
  Alphabetizes a list of strings using the default character code
  (ASCII/Unicode) order, but performs a case-insensitive comparison
  by using str.lower as the sorting key.

  Args:
    data_list (list): The list of strings to sort.

  Returns:
    list: A new sorted list.
  """
  return sorted(data_list, key=str.lower)

def merge_lists(list1, list2, pos):
    start = list1[:pos]
    
    smashed_item = list1[pos] + list2[0]

    end = list2[1:]
    
    return start + [smashed_item] + end

def crop_lst(lst, croppos, rev=False):
    croppos = int(croppos)
    retlst = []
    if not rev:
        if croppos >= len(lst):
            return(lst)
        else:
            for i in range (croppos):
                retlst.append(lst[i])

    else:
        croppos = len(lst)-croppos
        lst.reverse()
        if croppos > len(lst):
            return(lst)
        else:
            for i in range (croppos):
                retlst.append(lst[i])
            retlst.reverse()
            
        

    return(retlst)
