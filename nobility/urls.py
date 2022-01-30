from django.urls import path
from .models import Ticket
from . import views

home_list_view = views.HomeListView.as_view(
    queryset=Ticket.objects.order_by("-creationDate")[:10],
    context_object_name="tickets",
    template_name="nobility/home.html",
)

urlpatterns = [
    path("", home_list_view, name="home"),
    path("ticket/<ticket>", views.ticket, name="ticket"),
    path("editTicket/<ticket>", views.editTicket, name="editTicket"),
    path("changeStateOf/<ticket>", views.changeStateOf, name="changeState"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("add/", views.addTicket, name="add"),
    path("part/<part>", views.part, name="part"),
    path("addPart/<ticket>", views.addPart, name="addPart"),
    path("note/<ticket>", views.note, name="note"),
    path("searchResults/", views.SearchResultsView.as_view(), name="searchResults"),
]