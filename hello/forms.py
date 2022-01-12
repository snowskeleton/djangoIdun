from django import forms
from hello.models import Part, Ticket
from hello.longLists import parts
from hello.utils import fetchPartsFor

class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('serial', 'model', 'assetTag', 'customer',)

class PartCreateForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ('cost', 'replaced', 'mpn')

class PartAddForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs) #calls standard init
        print(args)
        lib = fetchPartsFor(args)
        # some = fetchPartsFor('Dell 3100 (Touch, +USB)')
        self.fields['parts'] = forms.ChoiceField(
        choices=lib)

    # class Meta:
    #     model = Part
    #     fields = ('name',)