from django.db import models
from django.utils import timezone
from datetime import datetime

class Ticket(models.Model):

    creationDate = models.DateTimeField("date logged")
    serialNumber = models.CharField(max_length=30, null=True, blank=True)
    modelNumber = models.CharField(max_length=30, null=True, blank=True, choices=([('FR', 'Freshman')]))
    assetTag = models.CharField(max_length=30, null=True, blank=True)
    customer = models.CharField(max_length=30, null=True, blank=False)
    # parts: list
    # notes: list
    def __str__(self):
        """Returns a string representation of a message."""
        date = timezone.localtime(self.log_date)
        return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}"
