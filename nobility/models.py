from django.db import models
from django.conf import settings
from django.db.models import Q

from royal.settings import EXPORT_PATH
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
        choices=longLists.states,
        default='New'
    )
    model = models.CharField(
        max_length=90,
        null=True,
        blank=True,
        choices=longLists.devices,
    )

    def updateState(self, request):
        ticket = self
        ticket.state = request.POST['state']
        ticket.save()
        log = f"Status changed to [{ticket.state}]."
        Note.log(ticket, log, request)
        return ticket

    # accepts HTTP request object. uses details of said object to update fields of self
    # this will have to incorporate validation logic if I ever want to track when something
    ##was updated
    def updateWith(self, request):
        post = request.POST
        self.serial = post['serial']
        self.model = post['model']
        self.assetTag = post['assetTag']
        self.customer = post['customer']
        self.claim = post['claim']
        self.state = post['state']
        self.save()
        return self

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
        return '; '.join(prettyParts) if len(prettyParts) > 0 else '--none--'

    # marks all parts for self as Ordered
    def orderAll(self, user):
        for part in self.parts():
            if part.ordered == False:
                part.ordered = True
                Note.log(part.ticket, f"Ordered [{part.name}].", user=user)
                part.save()
    
    # marks all parts for self as Replaced
    def replaceAll(self, user):
        for part in self.parts():
            if part.replaced == False:
                part.replaced = True
                Note.log(part.ticket, f"Replaced [{part.name}].", user=user)
                part.save()

    @classmethod
    def csvExport(self, queryset=None):
        import csv
        header = [ 'id',
            'model',
            'serial',
            'asset',
            'school',
            'status',
            'cost',
            'date',
            'parts',
            ]
        with open(f'{EXPORT_PATH}/export.csv', 'w+') as f:
            writer = csv.writer(f)
            writer.writerow(header)

            tickets = Ticket.objects.all() if queryset == None else Ticket.objects.filter(queryset)
            for ticket in tickets:
                data = ticket.__list__()
                writer = csv.writer(f)
                writer.writerow(data)

    def __str__(self):
        return "#" + self.paddedID()

    def __list__(self):
        return [
            f'{self.id}',
            f'{self.model}',
            f'{self.serial}',
            f'{self.assetTag}',
            f'{self.customer}',
            f'{self.state}',
            f'{self.cost()}',
            f'{self.creationDate:%Y-%m-%d %H:%M}',
            f'{self.prettyParts()}',
            ]


class Part(models.Model):
    @classmethod
    def fromID(self, part):
        return Part.objects.get(id=part)

    # accepts ticket() and part{} (part as dictionary; see longLists.py for examples).
    ## returns Part() with values from part{}
    @classmethod
    def spawn(self, ticket, part, request):
        return Part.objects.create(
        cost = part["cost"] if part["cost"] else 0,
        name = part["name"],
        mpn = part["mpn"] if part["mpn"] else '--blank--',
        sku = part["sku"] if part["sku"] else '--blank--',
        reason = request.POST["reason"] if request.POST["reason"] else 'Damaged by student',
        ticket = ticket,
        ordered = False,
        replaced = False,
        )

    name = models.CharField(max_length=127)
    cost = models.FloatField(max_length=12, null=True)
    ordered = models.BooleanField(default=False)
    replaced = models.BooleanField(default=False)
    mpn = models.CharField(max_length=24, null=True)
    sku = models.CharField(max_length=24, null=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    reason = models.CharField(max_length=127, null=True)

    def needed(self):
        return True if self.replaced == False else False

    def __list__(self):
        return [
            f'{self.id}',
            f'{self.name}',
            f'{self.cost}',
            f'{self.ordered}',
            f'{self.replaced}',
            f'{self.mpn}',
            f'{self.sku}',
            f'{self.ticket}',
            f'{self.reason}',
            ]

    @classmethod
    def csvExport(self, queryset=None):
        import csv
        header = [
            'id',
            'name',
            'cost',
            'ordered',
            'replaced',
            'mpn',
            'sku',
            'ticket',
            'reason',
            ]
        with open(f'{EXPORT_PATH}/export.csv', 'w+') as f:
            writer = csv.writer(f)
            writer.writerow(header)

            parts = Part.objects.all() if queryset == None else Part.objects.filter(queryset)
            for part in parts:
                writer = csv.writer(f)
                writer.writerow(part.__list__())

class Device(models.Model):
    model = models.CharField(max_length=127)


class Note(models.Model):
    body = models.TextField()
    date = models.DateTimeField("date created", auto_now_add=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    # accepts HTTP request, text string, and ticket() object. creates note for ticket with string
    @classmethod
    def log(self, ticket, body, request=None, user=None):
        Note.objects.create(
        body=body,
        ticket=ticket,
        user=(request.user if request else user)
        )
    

class AdvancedQuery(models.Model):
    tag = models.CharField(max_length=127, null=True, blank=True)
    value = models.CharField(max_length=127, null=True, blank=True)

    def query(self):
        return Q(**{self.tag + '__icontains': self.value })

    def __str__(self):
        return f'{self.tag}'