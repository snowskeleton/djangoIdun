from django.db import models
from django.utils import timezone
from hello.longLists import devices, parts
from hello.utils import fetchPartsFor
# from django.contrib.auth.models import User


class Ticket(models.Model):

    creationDate = models.DateTimeField("date logged", auto_now_add=True)
    serial = models.CharField(max_length=30, null=True, blank=True)
    model = models.CharField(
        max_length=90,
        null=True,
        blank=True,
        choices=devices,
    )
    parts = models.CharField(
        max_length=127,
        null=False,
        blank=False,
        choices=fetchPartsFor(f'{model}')
    )
    assetTag = models.CharField(max_length=30, null=True, blank=True)
    customer = models.CharField(max_length=30, null=True, blank=False)

    def partsToAdd(self):
        for (key, value) in parts.items():
            if key == self.model:
                return str(value)
        return parts.get('Generic') #return generic parts if the above didn't match anything


    def __str__(self):
        return f"{self.message}"

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