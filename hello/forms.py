from tkinter import Button
from django import forms
from hello.models import Ticket

class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('serial', 'model', 'assetTag', 'customer',)

class PartsForm(forms.Form): #Note that it is not inheriting from forms.ModelForm

    def __init__(self, ticket, *args, **kwargs):
        super(PartsForm, self).__init__(*args, **kwargs)        
        parts = []
        for part in ticket.partsPossible():
            parts.append((part['name'], part['name']))
        self.fields['parts'] = forms.ChoiceField(choices=parts)
    class Meta:
        fields = ('parts',)

class SearchForm(forms.Form):
    q = forms.CharField(label='Search', max_length=127)


class DeleteButton(forms.Form):
    button = forms.CharField(required=False)