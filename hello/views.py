from typing import List
from django.utils.timezone import datetime
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import FormView, ListView

from hello.forms import PartAddForm, TicketCreateForm, SearchForm
from hello.models import Ticket

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

class SearchView(FormView):
    template_name = 'search.html'
    form_class = SearchForm

def search(request):
    form = SearchForm(request.GET or request.POST)

    if request.method == "POST":
        pass
    else:
        return render(request, "hello/search.html", {"form": form})


def addPartToTicket(request, ticket):
    ticket = Ticket.hydrate(ticket)
    form = PartAddForm(request.POST or None, ticket.model)

    if request.method == "POST":
        pass
    else:
        return render(request, "hello/addPart.html", {"form": form, "model": ticket})