# from turtle import down
from django.utils.timezone import datetime
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
# import os
from django.http.response import HttpResponse

from royal.settings import EXPORT_PATH

from .forms import *
from .models import Ticket, Part, Note
from .ncsv import *


class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)

        return context


# GET: accepts ticket number (ticket.id). returns page with ticket details
# POST: accepts ticket number and uses request.POST['action'] item. returns page redirect to indicated 'action'
@login_required
def ticket(request, ticket):
    ticket = Ticket.fromID(ticket)
    form = ButtonButton(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        if request.POST['action'] == 'Add Part':
            return redirect(f"/addPart/{ticket.id}")
        if request.POST['action'] == 'Add Note':
            return redirect(f"/note/{ticket.id}")
        if request.POST['action'] == 'Edit':
            return redirect(f"/editTicket/{ticket.id}")

    return render(request, "nobility/ticket.html", {'ticket': ticket })


# GET: accepts ticket number (ticket.id). returns part addition page
# POST: accepts ticket number and uses request.POST['parts'] item. adds part to database, saves note to ticket,
## and redirects to 'ticket()'
@login_required
def addPart(request, ticket):
    ticket = Ticket.fromID(ticket)
    form = PartsForm(ticket=ticket)

    if request.method == "POST":
        for part in ticket.partsPossible():
            if part['name'] == request.POST['parts']:
                Part.spawn(ticket, part)
                Note.objects.create(
                    body=f"[{part['name']}] added.",
                    ticket=ticket,
                    user=request.user
                    )
        return redirect(f"/ticket/{ticket.id}")

    return render(request, "nobility/addPart.html", { 'form': form, 'ticket': ticket})


# GET: accepts ticket number (ticket.id). returns note creation page
# POST: accepts ticket number and uses NoteForm() for ticket body. redirects ticket page
@login_required
def note(request, ticket):
    ticket = Ticket.fromID(ticket)
    form = NoteForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        note = form.save(commit=False)
        note.user = request.user
        note.ticket = ticket
        note.save()
        return redirect(f"/ticket/{note.ticket.id}")

    return render(request, "nobility/note.html", { 'form': form, 'ticket': ticket})


# GET: accepts part number (part.id). returns parts editing page
# POST: accepts part number and uses request.POST['action'] item. performs indicated action,
## adds note to ticket, and redirects to ticket page
@login_required
def part(request, part):
    part = Part.fromID(part) #TODO: make a part version of Ticket.fromID(ticket)
    form = ButtonButton(request.POST or None)
    posOrNeg = True

    if request.method == 'POST' and form.is_valid():
        action = request.POST['action']

        if action == 'Order':
            part.ordered ^= True
            posOrNeg = part.ordered
            part.save()

        if action == 'Replace':
            part.replaced ^= True
            posOrNeg = part.replaced
            part.save()

        if action == 'Delete':
            part.delete()
            posOrNeg = False


        body = [
            f"{'' if posOrNeg else '— '}", # TODO: something better. I hate this line
            f"{action}",
            f"{'d' if action != 'Order' else 'ed'} ",
            f" [{part.name}].",
        ]
        Note.log(part.ticket, ''.join(body), request)
        return redirect(f"/ticket/{part.ticket.id}")

    return render(request, "nobility/part.html", {'form': form , 'part': part})


# GET: accepts nothing (except request). returns page with TicketCreateForm()
# POST: uses TicketCreateForm() to generate ticket. redirects to ticket page.
@login_required
def addTicket(request):
    form = TicketCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        ticket = form.save(commit=False)
        ticket.save()
        return redirect(f"/ticket/{ticket.id}")

    return render(request, "nobility/addTicket.html", {"form": form})


# GET: accepts ticket number (ticket.id). returns page with TicketEditForm()
# POST: accepts ticket number and uses TicketEditForm() to update ticket. redirects to ticket page
@login_required
def editTicket(request, ticket):
    ticket = Ticket.fromID(ticket)
    form = TicketEditForm(ticket=ticket)

    if request.method == "POST":
        ticket = ticket.updateWith(request)
        return redirect(f"/ticket/{ticket.id}")

    return render(request, "nobility/editTicket.html", {"form": form, "ticket": ticket})

# GET: accepts ticket number (ticket.id). returns page with ChangeStateOfForm()
# POST: acceptes ticket number and uses request.POST['state'] item to update ticket state.
## redirects to ticket page
@login_required
def changeStateOf(request, ticket):
    ticket = Ticket.fromID(ticket)
    form = ChangeStateOfForm(ticket=ticket)

    if request.method == "POST":
        ticket = ticket.updateState(request)
        return redirect(f"/ticket/{ticket.id}")

    return render(request, "nobility/changeStateOf.html", {"form": form, "ticket": ticket})


# GET: accepts  nothing and uses request.GET['q'] to fetch objects from database. returns Ticket() list
def searchResultsView(request):
    query = request.GET['q']
    object_list = Ticket.objects.filter((
        Q(id__icontains=query) |
        Q(serial__icontains=query) |
        Q(model__icontains=query) |
        Q(claim__icontains=query) |
        Q(customer__icontains=query)
        ))

    tickets = []
    for ob in object_list:
        if ob.state in request.GET.getlist('state'):
            tickets.append(object_list.get(id=ob.id))

    return render(request, "nobility/searchResults.html", {"tickets": tickets})


def export(request):
    if request.method == "POST":
        return download_file(request)
    return render(request, "nobility/export.html")


# GET: accepts nothing and uses request params to build a CSV and provide a download link
# TODO: make this accept paramaters by which to filter the csv
def download_file(request): # why am I passing in request if I'm not using it?
    # creates a new .csv file with the requested information
    req = NCSV(request)

    # declare the type of content (text/csv) in the HTTP header,
    ##then attach the location of the file to be served,
    ##which will be treated as downloadable thanks to
    ##setting the content type (text/csv).
    with open(req.filepath(), 'r') as path:
        response = HttpResponse(path, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={req.filename}'

        return response


# GET: accepts nothing. returns page with LoginForm()
# POST: accepts nothing and uses LoginForm() to authenticate the user. redirects to home page ##TODO: redirect to 'next' page
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

    return render(request, "nobility/login.html", {"form": form})


# GET: accepts nothing. logs request.user out and redirects to login page
# POST: accepts nothing. does nothing. returns nothing
def logout_view(request):
    logout(request)

    return redirect("/login/")