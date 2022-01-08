from django import forms
from hello.models import Part, Ticket

class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('serial', 'model', 'assetTag', 'customer',)

class PartCreateForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ('cost', 'replaced', 'mpn')