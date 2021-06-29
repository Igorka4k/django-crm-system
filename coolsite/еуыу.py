a = {1: "раз", 2: "два", 3: "три"}
b = {4: "чет", 5: "пять"}
# a = list(a.items())
# b = dict(list(b.items()))
for key, val in b.items():
    a[key] = val

print(a)
