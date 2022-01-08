from django.test import TestCase
from models import Ticket

# Create your tests here.
class TestViews(TestCase):

    def setUpClass(cls):
        import manage
        manage.makemigrations()
        manage.migrate()

    def setUp(self):
        Ticket.objects.create(serial="abc 123", model="the bestest", assetTag="8675309", customer="rudolph")

    def test_makeTicket(self):
        self.assertIsNotNone(Ticket.objects.get(serial="abc 123"))
        print("done")

if __name__ == '__main__':
    TestCase.main()