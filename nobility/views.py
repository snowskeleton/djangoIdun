from django.utils.timezone import datetime
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import *
from .models import Ticket, Part, Note


class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context


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


@login_required
def part(request, part):
    part = Part.objects.filter(id=part)[0]
    form = ButtonButton(request.POST or None)
    posOrNeg = True

    if request.method == 'POST' and form.is_valid():
        if request.POST['action'] == 'Order':
            part.ordered ^= True
            posOrNeg = part.ordered
            part.save()

        if request.POST['action'] == 'Replace':
            part.replaced ^= True
            posOrNeg = part.replaced
            part.save()

        if request.POST['action'] == 'Delete':
            part.delete()
            posOrNeg = False

        Note.objects.create(
        body=f"{'' if posOrNeg else '— '}" +
        f"{request.POST['action']}" +
        f"{'d' if request.POST['action'] != 'Order' else 'ed'} " +
        " [{part.name}].",
        # the above dynamically adds either "d" or "ed" to the 'action', depending on grammar
        ticket=part.ticket,
        user=request.user)
        return redirect(f"/ticket/{part.ticket.id}")

    return render(request, "nobility/part.html", {'form': form , 'part': part})


@login_required
def addTicket(request):
    form = TicketCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        ticket = form.save(commit=False)
        ticket.creationDate = datetime.now()
        ticket.state = "New"
        ticket.save()
        return redirect(f"/ticket/{ticket.id}")

    return render(request, "nobility/addTicket.html", {"form": form})


@login_required
def editTicket(request, ticket):
    ticket = Ticket.fromID(ticket)
    form = TicketEditForm(ticket=ticket)

    if request.method == "POST":
        post = request.POST
        ticket.serial = post['serial']
        ticket.model = post['model']
        ticket.assetTag = post['assetTag']
        ticket.customer = post['customer']
        ticket.claim = post['claim']
        ticket.state = post['state']
        ticket.save()
        return redirect(f"/ticket/{ticket.id}")

    return render(request, "nobility/editTicket.html", {"form": form, "ticket": ticket})

@login_required
def changeStateOf(request, ticket):
    ticket = Ticket.fromID(ticket)
    form = ChangeStateOfForm(ticket=ticket)

    if request.method == "POST":
        ticket.state = request.POST['state']
        ticket.save()
        Note.objects.create(
        body=f"{request.user} changed status to [{request.POST['state']}].",
        ticket=ticket,
        user=request.user
        )
        return redirect(f"/ticket/{ticket.id}")

    return render(request, "nobility/changeStateOf.html", {"form": form, "ticket": ticket})

class SearchResultsView(ListView):
    model = Ticket
    template_name = 'searchResults.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Ticket.objects.filter(
           (Q(id__icontains=query ) |
            Q(serial__icontains=query) |
            Q(model__icontains=query) |
            Q(claim__icontains=query) |
            Q(customer__icontains=query))
            )

        otherList = []
        for ob in object_list:
            if ob.state in self.request.GET.getlist('state'):
                otherList.append(object_list.get(id=ob.id))

        return otherList

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

def logout_view(request):
    logout(request)
    return redirect("/login/")