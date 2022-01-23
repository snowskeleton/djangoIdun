from logging import raiseExceptions
from random import choice
from django import forms
from hello.models import Part, Ticket#, UselessModel
from hello.longLists import parts, devices
from hello.utils import fetchPartsFor

class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('serial', 'model', 'assetTag', 'customer',)

class AddPartsForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('serial',)

class PartsForm(forms.Form): #Note that it is not inheriting from forms.ModelForm

    # fields['parts'] = forms.ChoiceField(choices=self.ticket.partsPossible())
    def __init__(self, ticket, *args, **kwargs):
        super(PartsForm, self).__init__(*args, **kwargs)        
        parts = []
        for part in ticket.partsPossible():
            parts.append((part, part['name']))
        self.fields['parts'] = forms.ChoiceField(choices=parts)
    class Meta:
        fields = ('parts',)

class PartCreateForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ('cost', 'replaced', 'mpn',)

class SearchForm(forms.Form):
    q = forms.CharField(label='Search', max_length=127)