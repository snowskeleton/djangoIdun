from .models import Ticket
from django.db.models import Q

class NQuery():

    # accepts HTTP request. returns QuerySet object filtered by params in request if possible, otherwise returns all Ticket()s.
    @classmethod
    def tickets(self, request):
        try:
            get = request.GET
        except:
            print('error: NQeuery.tickets() failed to find request.GET. returned all() instead')
            return Ticket.objects.all()

        query = get['q']
        queries = (( # effectly a 'full-text' search, but sqlite is special
            Q(id__icontains=query) |
            Q(serial__icontains=query) |
            Q(model__icontains=query) |
            Q(claim__icontains=query) |
            Q(customer__icontains=query)) &
            Q(state__in=get.getlist('state'))
        )

        fields = [ 
            [None, 'serial', ''],
            [None, 'model', ''],
            [None, 'asset', ''],
            [None, 'customer', ''],
        ]
        for field in fields:
            if f'{field[1]}' in get.getlist('toggle'):
                field[0] = True
                field[2] = f'{get[field[1]]}'
                queries = queries & Q(**({f'{field[1]}'+'__icontains': f'{field[2]}'}))
            else:
                field[0] = False

        return Ticket.objects.filter(queries)
