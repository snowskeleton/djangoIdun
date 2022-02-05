from .models import *

class NCSV():
    
    def __init__(self, request):
        self.table = request.POST['table']
        self.filename = 'export.csv'
        # params = request.POST['search criteria']
        if self.table == 'Tickets':
            Ticket.csvExport()
        if self.table == 'Parts':
            Part.csvExport()

            #     {
            # 'filename': '<filename, probably .csv>',
            # 'table': 'Ticket/Part',
            # 'search criteria': { # dict of criteria, with "'field': 'value'" format
            #     'customer': '<school name>',
            #     'model': '<model>',
            #     #etc
            #     }
            # }

    @classmethod
    def valid(request):
        return True # I'll fix this later

    def filepath(self):
        return EXPORT_PATH + self.filename
    
    