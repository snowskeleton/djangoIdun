from typing import List
from django.utils.timezone import datetime
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import ListView

from hello.forms import PartAddForm, TicketCreateForm
from hello.models import Ticket
from hello.utils import hydrateTicket

# def home(request):
#     return render(request, "hello/home.html")

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        print(context)
        return context


def ticket(request, ticket):
    return render(request, "hello/ticket.html", { 'tickets': Ticket.objects.filter(id=ticket)})


def addTicket(request):
    form = TicketCreateForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.creationDate = datetime.now()
            ticket.save()
            return redirect(f"/ticket/{ticket.id}")
    else:
        return render(request, "hello/addTicket.html", {"form": form})

def addPartToTicket(request, ticket):
    ticket = hydrateTicket(ticket)
    print(ticket)
    form = PartAddForm(request.POST or None, ticket.model)

    if request.method == "POST":
        pass
    else:
        return render(request, "hello/addPart.html", {"form": form, "model": ticket})