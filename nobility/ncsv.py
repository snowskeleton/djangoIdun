from .models import *

class NCSV():
    
    def __init__(self, request):
        self.table = request.GET['table']
        print(self.table)
        self.filename = 'export.csv'
        if self.table == 'tickets':
            Ticket.csvExport(request)
        if self.table == 'parts':
            Part.csvExport(request)

    @classmethod
    def valid(request):
        return True # I'll fix this later

    def filepath(self):
        return EXPORT_PATH + self.filename
    
    