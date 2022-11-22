import json
import zlib

import bmasm

name = input("Library name: ") + ".bex"
foc = input("File or direct code (F/D): ").capitalize()
while foc not in ["F", "D"]: foc = input("File or direct code (F/D): ").capitalize()
if foc == "F":
    with open(input("File path: "), "r") as f:
        tokens = bmasm.analyse(f.read())
if foc == "D":
    tokens = bmasm.analyse(input("Code: "))

print(bytes(json.dumps(tokens), encoding="utf-8"))

with open(name, "wb") as f:
    f.write(zlib.compress(bytes(json.dumps(tokens), encoding="utf-8")))
    
print("Completed successfully")
