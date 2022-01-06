from django import forms
from hello.models import Ticket

class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('creationDate', 'serialNumber', 'modelNumber', 'assetTag', 'customer',)