from django.db import models
from hello.longLists import devices, parts



class Ticket(models.Model):

    creationDate = models.DateTimeField("date logged", auto_now_add=True)
    serial = models.CharField(max_length=30, null=True, blank=True)
    model = models.CharField(
        max_length=90,
        null=True,
        blank=True,
        choices=devices,
    )
    assetTag = models.CharField(max_length=30, null=True, blank=True)
    customer = models.CharField(max_length=30, null=True, blank=False)

    def parts(self):
        return Part.objects.filter(ticket=self)

    def prettyParts(self):
        parts = []
        _parts = Part.objects.filter(ticket=self)

        for part in _parts:
            parts.append(part.name)
        return parts if len(parts) > 0 else '--none--'

    def partsToAdd(self):
        for (key, value) in parts.items():
            if key == self.model:
                return str(value)
        return parts.get('Generic') #return generic parts if the above didn't match anything
    
    def partsPossible(self):
        arr = []
        for (key, value) in parts.items():
            if key == self.model:
                arr = value
        if len(arr) > 0:
            return arr
        else:
            for (key, value) in parts.items():
                if key == 'Generic':
                    arr = value
            return arr

    def partsNeeded(self):
        arr = []
        for part in self.parts:
            if part.replaced != True:
                arr.append(part)
        return arr

    def partsReplaced(self):
        arr = []
        for part in self.parts:
            if part.replaced != False:
                arr.append(part)
        return arr


    # def __str__(self):
    #     return f"{self.message}"

class Device(models.Model):
    model = models.CharField(max_length=127)


class Note(models.Model):
    body = models.TextField()
    date = models.DateTimeField("date created", auto_now_add=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.PROTECT)


class Part(models.Model):
    name = models.CharField(max_length=127)
    cost = models.FloatField(max_length=12)
    ordered = models.BooleanField(default=False)
    replaced = models.BooleanField(default=False)
    mpn = models.CharField(max_length=24)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    @classmethod
    def spawn(self, ticket, part):
        return Part(
        cost = part["cost"] if part["cost"] else 0,
        name = part["name"],
        mpn = part["mpn"] if part["mpn"] else "--blank--",
        ticket = ticket,
        ordered = False,
        replaced = False,

        ).save()