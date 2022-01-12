from hello.longLists import parts
from hello.models import Ticket

def fetchPartsFor(model):
    for (key, value) in parts.items():
        if key == model:
            return value

def hydrateTicket(num):
    return Ticket.objects.get(id=num)
# some = fetchPartsFor('Dell 3100 (Touch, +USB)')
# print(some)