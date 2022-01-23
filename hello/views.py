from typing import List
from django.utils.timezone import datetime
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q

from .forms import AddPartsForm, TicketCreateForm, PartsForm
from .models import Ticket, Part


class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context


# def form_handle(request):
#     form = PartsForm()
#     if request.method=='POST':
#         form = PartsForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             #now in the object cd, you have the form as a dictionary.
#             part = cd.get('part')



def ticket(request, ticket):
    ticket = Ticket.objects.filter(id=ticket)[0]
    form = PartsForm(ticket=ticket) #.__init__(self, ticket=ticket)

    if request.method == "POST":
        form = PartsForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            for val in ticket.partsPossible():
                if val["name"] == cd:
                    Part.spawn(ticket, val)
                else:
                    pass #and say something about it not being valid.

            return redirect(f"/ticket/{ticket.id}")
    else:
        return render(request, "hello/ticket.html", { 'form': form, 'ticket': ticket})
    # return render(request, "hello/ticket.html", { 'form': form, 'ticket': Ticket.objects.filter(id=ticket)[0]})


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
    form = AddPartsForm(request.POST or None, ticket)

    if request.method == "POST":
        pass
    else:
        return render(request, "hello/addPart.html", {"form": form, "model": ticket})