from django.db import models
from . import longLists


class Ticket(models.Model):

    creationDate = models.DateTimeField("date logged", auto_now_add=True)
    serial = models.CharField(max_length=30, null=True, blank=True)
    assetTag = models.CharField(max_length=30, null=True, blank=True)
    customer = models.CharField(max_length=30, null=True, blank=False)
    model = models.CharField(
        max_length=90,
        null=True,
        blank=True,
        choices=longLists.devices,
    )
  

    def parts(self):
        return Part.objects.filter(ticket=self)

    def prettyParts(self):
        prettyParts = []
        for part in self.parts():
            prettyParts.append(part.name)
        return ', '.join(prettyParts) if len(prettyParts) > 0 else '--none--'

    def partsToAdd(self):
        for (key, value) in longLists.parts.items():
            if key == self.model:
                return str(value)
        return longLists.parts.get('Generic') #return generic parts if the above didn't match anything
    
    def partsPossible(self):
        arr = []
        for (key, value) in longLists.parts.items():
            if key == self.model:
                arr = value
        if len(arr) > 0:
            return arr
        #else
        for (key, value) in longLists.parts.items():
            if key == 'Generic':
                arr = value
        return arr

    def partsNeeded(self):
        return self.parts().filter(replaced=False)

    def partsUsed(self):
        return self.parts().filter(replaced=True)


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
    sku = models.CharField(max_length=24)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    def needed(self):
        return True if self.replaced == False else False

    @classmethod
    def spawn(self, ticket, part):
        return Part(
        cost = part["cost"] if part["cost"] else 0,
        name = part["name"],
        mpn = part["mpn"] if part["mpn"] else "--blank--",
        sku = part["sku"] if part["sku"] else "--blank--",
        ticket = ticket,
        ordered = False,
        replaced = False,
        ).save()