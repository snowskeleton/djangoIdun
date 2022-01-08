from django.urls import path
from hello.models import Part, Ticket
import hello.views

home_list_view = hello.views.HomeListView.as_view(
    queryset=Ticket.objects.order_by("-creationDate")[:5],
    context_object_name="message_list",
    template_name="hello/home.html",
)

urlpatterns = [
    path("", home_list_view, name="home"),
    path("hello/<name>", hello.views.hello_there, name="hello_there"),
    path("ticket/<ticket>", hello.views.ticket, name="ticket"),
    path("about/", hello.views.about, name="about"),
    path("contact/", hello.views.contact, name="contact"),
    path("log/", hello.views.log_message, name="log"),
]