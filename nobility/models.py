from django.db import models
from django.conf import settings
from django.http import HttpResponse
from . import longLists


class Ticket(models.Model):
    # acceptes ticket number (ticket.id). returns Ticket() object
    @classmethod
    def fromID(self, ticket):
        return Ticket.objects.get(id=ticket)

    creationDate = models.DateTimeField("date logged", auto_now_add=True)
    serial = models.CharField(max_length=30, null=True, blank=True)
    assetTag = models.CharField(max_length=30, null=True, blank=True)
    customer = models.CharField(max_length=30, null=True, blank=False)
    claim = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(
        max_length=90,
        null=True,
        blank=True,
        choices=longLists.states
    )
    model = models.CharField(
        max_length=90,
        null=True,
        blank=True,
        choices=longLists.devices,
    )

    def notes(self):
        return Note.objects.filter(ticket=self).order_by('-date') #newest note on top

    def parts(self):
        return Part.objects.filter(ticket=self)
  
    def partsNeeded(self):
        return self.parts().filter(replaced=False)

    def partsUsed(self):
        return self.parts().filter(replaced=True)
    # attr. sum of all parts costs
    def cost(self):
        cost = 0.0
        for part in self.parts():
            cost += part.cost
        return "${:,.2f}".format(cost)

    # accepts nothing. returns ticket number (ticket.id) with zero padding (for UI purposes)
    def paddedID(self):
        f'{self.id:05}'
        return f'{self.id:05}'
    
    # accepts nothing. returns nubmer of Notes() associated with ticket (self) [used as a BOOL in HTML template]
    def hasNotes(self):
        return len(self.notes())

    # accepts nothing. returns list() of parts as dictionaries with 'parts == self.model'.
    ## returns generic list if no entry found
    def partsPossible(self):
        for (key, value) in longLists.parts.items():
            if key == self.model:
                return value
        return longLists.parts.get('Generic') #return generic parts if no model found

    # accepts nothing. returns string of all Parts() with 'ticket == self.id' (for UI purposes)
    def prettyParts(self):
        prettyParts = []
        for part in self.parts():
            prettyParts.append(part.name)
        return ', '.join(prettyParts) if len(prettyParts) > 0 else '--none--'

    @classmethod
    def csvExport(self):
        import csv
        header = [
            'id',
            'model',
            'serial',
            'asset',
            'school',
            'status',
            'cost',
            'date',
            'parts',
            ]
        with open('./downloads/export/export.csv', 'w+') as f:
            writer = csv.writer(f)
            writer.writerow(header)
        for ticket in Ticket.objects.all():
            data = [
                f'{ticket.id}',
                f'{ticket.model}',
                f'{ticket.serial}',
                f'{ticket.assetTag}',
                f'{ticket.customer}',
                f'{ticket.state}',
                f'{ticket.cost()}',
                f'{ticket.creationDate:%Y-%m-%d %H:%M}',
                f'{ticket.prettyParts()}',
                ]
            with open('./downloads/export/export.csv', 'a+') as f:
                writer = csv.writer(f)
                writer.writerow(data)

class Device(models.Model):
    model = models.CharField(max_length=127)


class Note(models.Model):
    body = models.TextField()
    date = models.DateTimeField("date created", auto_now_add=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    

class Part(models.Model):
    # accepts ticket() and part{} (part as dictionary; see longLists.py for examples).
    ## returns Part() with values from part{}
    @classmethod
    def spawn(self, ticket, part):
        return Part(
        cost = part["cost"] if part["cost"] else 0,
        name = part["name"],
        mpn = part["mpn"] if part["mpn"] else None,
        sku = part["sku"] if part["sku"] else None,
        ticket = ticket,
        ordered = False,
        replaced = False,
        ).save()

    name = models.CharField(max_length=127)
    cost = models.FloatField(max_length=12, null=True)
    ordered = models.BooleanField(default=False)
    replaced = models.BooleanField(default=False)
    mpn = models.CharField(max_length=24, null=True)
    sku = models.CharField(max_length=24, null=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def needed(self):
        return True if self.replaced == False else False