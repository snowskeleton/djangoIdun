from django.utils.timezone import datetime
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q

from .forms import NoteForm, TicketCreateForm, PartsForm, ButtonButton
from .models import Ticket, Part


class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context


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


def note(request, ticket):
    ticket = Ticket.whoamI(ticket)
    form = NoteForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        note = form.save(commit=False)
        note.ticket = ticket
        note.save()
        return redirect(f"/ticket/{note.ticket.id}")
    return render(request, "hello/note.html", { 'form': form, 'ticket': ticket})


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

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Ticket.objects.filter(
           Q(id__icontains=query)
        )
        return object_list