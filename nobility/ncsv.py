from .models import *

class NCSV():
    
    def __init__(self, request):
        self.table = request.POST['table']
        self.filename = 'export.csv'
        if self.table == 'Tickets':
            Ticket.csvExport()
        if self.table == 'Parts':
            Part.csvExport()

    @classmethod
    def valid(request):
        return True # I'll fix this later

    def filepath(self):
        return EXPORT_PATH + self.filename
    
    