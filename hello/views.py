from django.utils.timezone import datetime
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import NoteForm, TicketCreateForm, PartsForm, ButtonButton, LoginForm
from .models import Ticket, Part


class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context


@login_required
def ticket(request, ticket):
    ticket = Ticket.whoamI(ticket)
    form = ButtonButton(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        if request.POST['action'] == 'Add Part':
            return redirect(f"/addPart/{ticket.id}")
        if request.POST['action'] == 'Add Note':
            return redirect(f"/note/{ticket.id}")
        if request.POST['action'] == 'Change Status':
            pass
        # part.save()
        return redirect(f"/ticket/{ticket.id}")
    return render(request, "hello/ticket.html", {'ticket': ticket })


@login_required
def addPart(request, ticket):
    ticket = Ticket.whoamI(ticket)
    form = PartsForm(ticket=ticket)

    if request.method == "POST":
        for part in ticket.partsPossible():
            if part['name'] == request.POST['parts']:
                Part.spawn(ticket, part)
        return redirect(f"/ticket/{ticket.id}")
    else:
        return render(request, "hello/addPart.html", { 'form': form, 'ticket': ticket})


@login_required
def note(request, ticket):
    ticket = Ticket.whoamI(ticket)
    form = NoteForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        note = form.save(commit=False)
        note.ticket = ticket
        note.save()
        return redirect(f"/ticket/{note.ticket.id}")
    return render(request, "hello/note.html", { 'form': form, 'ticket': ticket})


@login_required
def part(request, part):
    part = Part.objects.filter(id=part)[0]
    form = ButtonButton(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        if request.POST['action'] == 'Order':
            part.ordered ^= True
            part.save()
        if request.POST['action'] == 'Replace':
            part.replaced ^= True
            part.save()
        if request.POST['action'] == 'Delete':
            part.delete()
        return redirect(f"/ticket/{part.ticket.id}")

    return render(request, "hello/part.html", {'form': form , 'part': part})

@login_required
def addTicket(request):
    form = TicketCreateForm(request.POST or None)

    print(form)
    if request.method == "POST" and form.is_valid():
        ticket = form.save(commit=False)
        ticket.creationDate = datetime.now()
        ticket.save()
        return redirect(f"/ticket/{ticket.id}")
    else:
        return render(request, "hello/addTicket.html", {"form": form})


class SearchResultsView(ListView):
    model = Ticket
    template_name = 'searchResults.html'

    @login_required
    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Ticket.objects.filter(
           Q(id__icontains=query)
        )
        return object_list

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate( request, username=username, password=password)
        if user == None:
            return 401
        else:
            login(request, user)
            return redirect("/")
    return render(request, "hello/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("/login/")