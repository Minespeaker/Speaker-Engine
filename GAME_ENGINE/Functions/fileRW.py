import os

def load(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()

    return(file_content)

def save(file_path, string):
    text_to_write = string
    norm_path = os.path.normpath(file_path)
    dirpath = os.path.dirname(norm_path)
    if dirpath:
        try:
            os.makedirs(dirpath, exist_ok=True)
        except Exception:
            pass

    with open(norm_path, "w", encoding="utf-8") as f:
        f.write(text_to_write)


def loadbin(file_path):
    with open(file_path, "rb") as f:
        file_content = f.read()

    return(file_content)

def savebin(file_path, string):
    text_to_write = string
    norm_path = os.path.normpath(file_path)
    dirpath = os.path.dirname(norm_path)
    if dirpath:
        try:
            os.makedirs(dirpath, exist_ok=True)
        except Exception:
            pass
    try:
        with open(norm_path, "wb") as f:
            f.write(text_to_write)
    except FileExistsError:
        with open(norm_path, "wbx") as f:
            f.write(text_to_write)
            
            
def recursive_scan(sep, dir, q, file=None, _parent=True):
    name = dir.split(sep)[-1]
    if file == None:
        file = {name: ({}, _parent)}
    files, headunpack = file[name]
    filen = {}
    for folder in [f for f in os.listdir(dir) if os.path.isdir(os.path.join(dir, f))]:
        foldername = folder
        if folder in files:
            contents, unpack = files[folder]
        else:
            contents = {}
            unpack = False
        childdata = recursive_scan(os.path.join(dir, folder), q, {foldername: (contents, unpack)}, False)
        contents, _ = childdata[foldername]
        filen[folder] = contents, unpack
    for file in [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]:
        filen[file] = loadbin(os.path.join(dir, file))
    filen = {name: (filen, headunpack)}
    if _parent:
        q.put(filen)
    return filen
