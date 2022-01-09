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
    path("hello/<name>", views.hello_there, name="hello_there"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("log/", views.log_message, name="log"),
]