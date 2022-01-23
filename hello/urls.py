from django.urls import path
from hello.models import Ticket
import hello.views as views

home_list_view = views.HomeListView.as_view(
    queryset=Ticket.objects.order_by("-creationDate")[:5],
    context_object_name="tickets",
    template_name="hello/home.html",
)

urlpatterns = [
    path("", home_list_view, name="home"),
    path("ticket/<ticket>", views.ticket, name="ticket"),
    path("add/", views.addTicket, name="add"),
    path("searchResults/", views.SearchResultsView.as_view(), name="searchResults"),
]