debug = True

def dprint(*args):
    from Functions.debug import debug
    try:
        if debug:
            print(args)
    except NameError:
        debug = False