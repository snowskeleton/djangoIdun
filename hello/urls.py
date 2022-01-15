from django.urls import path
from hello.models import Ticket
import hello.views as views

home_list_view = views.HomeListView.as_view(
    queryset=Ticket.objects.order_by("-creationDate")[:5],
    context_object_name="message_list",
    template_name="hello/home.html",
)
# ticket_view = views.TicketView.as_view(
#     queryset=Ticket.objects.filter(id=1),
#     context_object_name="ticketDetails",
#     template_name="hello/ticket.html",
# )

urlpatterns = [
    path("", home_list_view, name="home"),
    path("ticket/<ticket>", views.ticket, name="ticket"), #HERE I AM avocado
    path("addPart/<ticket>", views.addPartToTicket, name="addPart"),
    path("add/", views.addTicket, name="add"),
    path("searchResults/", views.SearchResultsView.as_view(), name="searchResults"),
    path("search/", views.SearchView.as_view(), name="search"),
]