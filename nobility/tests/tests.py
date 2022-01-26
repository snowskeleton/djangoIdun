from datetime import datetime
from django.test import TestCase
from models import Ticket

# Create your tests here.
class TestViews(TestCase):

    # def setUpClass():
    #     import manage
    #     manage.makemigrations()
    #     manage.migrate()

    def setUp(self):
        Ticket.objects.create(serial="abc 123", model="the bestest", assetTag="8675309", customer="rudolph")

    def test_makeTicket(self):
        self.assertIsNotNone(Ticket.objects.get(serial="abc 123"))
        from MOCK_DATA import test_data
        for thing in test_data:
            Ticket.objects.create(thing)
            

        Ticket.objects.create(
            creationDate=datetime.now(),
            model="ABc d fg/n",
            serial="42069",
            assetTag="000123",
            customer="Santa"
        )

if __name__ == '__main__':
    TestCase.main()