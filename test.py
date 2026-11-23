def checkPrime(num=int):
    import math
    if num in (2, 3):
        return True
    for n in range(math.floor(num**0.5)-1):
        if num/(n+2) == num//(n+2):
            return False
        print(f"Checking: {(n*10000000)/num}%")
    return True

print(sorted([0, 0, 1, 1, 2, 2, 3, -1]))