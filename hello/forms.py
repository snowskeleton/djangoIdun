from tkinter import Button
from django import forms
from hello.models import Note, Ticket

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


class ButtonButton(forms.Form):
    button = forms.CharField(required=False)


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('body',)


from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    # def clean(self):
    #     username = self.cleaned_data.get("username")
    #     password = self.cleaned_data.get('password')

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username=username)
        if not qs.exists():
            raise forms.ValidationError("This is an invalid user.")
        return username