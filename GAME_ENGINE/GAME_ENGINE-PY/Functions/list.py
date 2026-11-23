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