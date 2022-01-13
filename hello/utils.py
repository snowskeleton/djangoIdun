from hello.longLists import parts

def fetchPartsFor(model):
    for (key, value) in parts.items():
        if key == model:
            return value

# some = fetchPartsFor('Dell 3100 (Touch, +USB)')
# print(some)