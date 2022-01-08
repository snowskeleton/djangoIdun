from django.utils.timezone import datetime
from django.shortcuts import redirect
from hello.forms import TicketCreateForm
from hello.models import Ticket
from django.shortcuts import render
from django.views.generic import ListView

# def home(request):
#     return render(request, "hello/home.html")

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

def about(request):
    return render(request, "hello/about.html")

def contact(request):
    return render(request, "hello/contact.html")

def hello_there(request, name):
    return render(
        request,
        'hello/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

def ticket(request):

    return render(request, "hello/ticket.html")

def log_message(request):
    form = TicketCreateForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.creationDate = datetime.now()
            message.save()
            return redirect("home")
    else:
        return render(request, "hello/log_message.html", {"form": form})