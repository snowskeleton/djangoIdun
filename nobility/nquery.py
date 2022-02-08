from .models import Ticket, Part, AdvancedQuery
from django.db.models import Q

class NQuery():

    # accepts HTTP request.
    # returns QuerySet object filtered by params in request if possible,
    ##otherwise returns all Ticket()s.
    @classmethod
    def tickets(self, request):
        get = request.GET
        # run just the basic search before checking Advanced search fields.
        queries = self.simpleTickets(request)

        if get['action'] == 'Advance':

            _fields = [ 
                ['serial', ''],
                ['model', ''],
                ['asset', ''],
                ['customer', ''],
            ]
            fields = []
            for s in _fields:
                q = AdvancedQuery.objects.create(tag=f'{s[0]}')
                fields.append(q)
                
            for field in fields:
                if get[f'{field.tag}'] != '':
                    field.value = get[f'{field.tag}']
                    queries = queries & Q((field.query()))

        return Ticket.objects.filter(queries).order_by("-creationDate")


    def simpleTickets(request):
        try:
            get = request.GET
        except:
            print('error: NQeuery.simpleTickets() failed to parse request.GET. returned all() instead')
            return Ticket.objects.all()
        query = get['q']
        queries = (( # effectly a 'full-text' search, but sqlite is special
            Q(id__icontains=query) |
            Q(serial__icontains=query) |
            Q(model__icontains=query) |
            Q(assetTag__icontains=query) |
            Q(claim__icontains=query) |
            Q(customer__icontains=query)) &
            Q(state__in=get.getlist('state'))
        )
        return queries


    @classmethod
    def parts(self, request):
        try:
            get = request.GET
        except:
            print('error: NQeuery.parts() failed to parse request.GET. returned all() instead')
            return Part.objects.all()

        query = get['q']
        queries = (( # effectly a 'full-text' search, but sqlite is special
            Q(name__icontains=query) |
            Q(mpn__icontains=query) |
            Q(sku__icontains=query))
        )

        fields = [ 
            [None, 'name', ''],
            [None, 'mpn', ''],
            [None, 'sku', ''],
            [None, 'ordered', ''],
            [None, 'replaced', ''],
        ]
        for field in fields:
            if f'{field[1]}' in get.getlist('toggle'):
                field[0] = True
                field[2] = f'{get[field[1]]}'
                queries = queries & Q(**({f'{field[1]}'+'__icontains': f'{field[2]}'}))
            else:
                field[0] = False

        return Part.objects.filter(queries)