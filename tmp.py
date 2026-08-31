with open("GAME_ENGINE/main.py", "r") as f:
    code = f.read()
    code = list(code)
    
print(f"There are {len(code)} characters")

code = [i for i in code if i == "z"]

print(f"There are {len(code)} characters")