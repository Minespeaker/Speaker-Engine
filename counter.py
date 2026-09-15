import os
from os.path import join as pathjoin

def get_py_files(dir, _parent=True):
    idx = set()
    for obj in os.listdir(dir):
        if os.path.isfile(pathjoin(dir, obj)):
            if ".py" in obj:
                idx.add(pathjoin(dir, obj))
        elif os.path.isdir(pathjoin(dir, obj)):
            if obj not in ("__pycache__", ".vscode", ".venv", ".git"):
                subdir = get_py_files(pathjoin(dir, obj), False)
                for i in subdir:
                    idx.add(i)
        else:
            raise Exception("Fuck you")
        
    return idx
    
code = []
files = []

for i in get_py_files("/home/minespeaker/programs/Speaker-Engine/GAME_ENGINE"):
    files.append(i)
    with open(i, "r", encoding="utf-8") as f:
        code.append(f.read())
    f.close()
    
code = "".join(code)

print(f"There are {len(code)} characters")

letters = []

for letter in list("abcdefghijklmnopqrstuvwxyz1234567890-=`~'\"\\/,.<>[]{}!@#$%^&*()_+|?;: "):

    tmp = [i for i in code.lower() if i == letter]

    letters.append(len(tmp))
    
letters.sort()
letters.reverse()

for i in letters:
    print(f"There are {i} appearances of \"{letter}\"")
    
for file in files:
    print(file)
    
code = "".join(code)

print(f"There are {len(code)} characters")