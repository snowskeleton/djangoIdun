from django.db import models
# from django.contrib.auth.models import User

# from django.utils import timezone


class Ticket(models.Model):

    creationDate = models.DateTimeField("date logged", auto_now_add=True)
    serial = models.CharField(max_length=30, null=True, blank=True)
    model = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        choices=([("Dell3100Touch&USB", "Dell 3100 (Touch, +USB)")]),
    )
    assetTag = models.CharField(max_length=30, null=True, blank=True)
    customer = models.CharField(max_length=30, null=True, blank=False)
    # def __str__(self):
    #     """Returns a string representation of a message."""
    #     date = timezone.localtime(self.log_date)
    #     return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}"

    def __str__(self) -> str:
        return super().__str__()

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
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
