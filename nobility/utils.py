from .longLists import parts

# Usage: var = fetchPartsFor('Dell 3100 (Touch, +USB)')
def fetchPartsFor(model):
    for (key, value) in parts.items():
        if key == model:
            return value
