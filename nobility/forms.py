from django import forms
from .models import Note, Ticket
from django.contrib.auth import get_user_model

class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('serial', 'model', 'asset', 'customer',)


class TicketEditForm(forms.ModelForm):
    def __init__(self, ticket, *args, **kwargs):
        super(TicketEditForm, self).__init__(*args, **kwargs)        
        self.fields['serial'].initial = ticket.serial
        self.fields['model'].initial = ticket.model
        self.fields['asset'].initial = ticket.asset
        self.fields['customer'].initial = ticket.customer
        self.fields['claim'].initial = ticket.claim
        self.fields['state'].initial = ticket.state
    class Meta:
        model = Ticket
        fields = ('serial', 'model', 'asset', 'customer', 'claim', 'state',)


class ChangeStateOfForm(forms.ModelForm):
    def __init__(self, ticket, *args, **kwargs):
        super(ChangeStateOfForm, self).__init__(*args, **kwargs)        
        self.fields['state'].initial = ticket.state
    class Meta:
        model = Ticket
        fields = ('state',)


class PartsForm(forms.Form): #Note that it is not inheriting from forms.ModelForm
    def __init__(self, ticket, *args, **kwargs):
        super(PartsForm, self).__init__(*args, **kwargs)        
        parts = []
        for part in ticket.partsPossible():
            parts.append((part['name'], part['name']))
        self.fields['parts'] = forms.ChoiceField(choices=parts)
        self.fields['reason'] = forms.CharField(max_length=127, required=False)
    class Meta:
        fields = ('parts', 'reason',)


class SearchForm(forms.Form):
    q = forms.CharField(label='Search', max_length=127)


class ButtonButton(forms.Form):
    button = forms.CharField(required=False)


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('body',)


User = get_user_model() #does this really need to be here?

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username=username)
        if not qs.exists():
            raise forms.ValidationError("This is an invalid user.")
        return username