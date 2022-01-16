from typing import List
from django.http import request
from django.utils.timezone import datetime
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import FormView, ListView
from django.db.models import Q

from hello.forms import ChangePartsOnTicketForm, TicketCreateForm, SearchForm
from hello.models import Ticket

# def home(request):
#     return render(request, "hello/home.html")

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context


def ticket(request, ticket):
    return render(request, "hello/ticket.html", { 'ticket': Ticket.objects.filter(id=ticket)[0]})


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


class SearchResultsView(ListView):
    model = Ticket
    template_name = 'searchResults.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Ticket.objects.filter(
           Q(id__icontains=query)
        )
        return object_list


def changePartsOnTicket(request, ticket):
    ticket = Ticket.objects.filter(id=ticket)
    form = ChangePartsOnTicketForm(request.POST or None, ticket.model)
    form.model = ticket.model

    if request.method == "POST":
        pass
    else:
        return render(request, "hello/addPart.html", {"form": form, "model": ticket})