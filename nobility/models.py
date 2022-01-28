from django.db import models
from django.conf import settings
from . import longLists
from django.contrib.auth.models import User


class Ticket(models.Model):

    creationDate = models.DateTimeField("date logged", auto_now_add=True)
    serial = models.CharField(max_length=30, null=True, blank=True)
    assetTag = models.CharField(max_length=30, null=True, blank=True)
    customer = models.CharField(max_length=30, null=True, blank=False)
    claim = models.CharField(max_length=30, null=True, blank=False)
    model = models.CharField(
        max_length=90,
        null=True,
        blank=True,
        choices=longLists.devices,
    )
  
    @classmethod
    def whoamI(self, ticket):
        return Ticket.objects.filter(id=ticket)[0]

    def partsPossible(self):
        for (key, value) in longLists.parts.items():
            if key == self.model:
                return value
        return longLists.parts.get('Generic') #return generic parts if no model found

    def notes(self):
        return Note.objects.filter(ticket=self).order_by('-date') #newest note on top

    def parts(self):
        return Part.objects.filter(ticket=self)

    def prettyParts(self):
        prettyParts = []
        for part in self.parts():
            prettyParts.append(part.name)
        return ', '.join(prettyParts) if len(prettyParts) > 0 else '--none--'

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    
    def tableDate(self):

        pass


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