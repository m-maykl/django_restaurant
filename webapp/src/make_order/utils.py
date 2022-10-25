from make_order.models import Printer
from django.core.exceptions import BadRequest

def add_printers():
    if len(Printer.objects.all()) == 0:
            Printer.objects.create(name='Kyiv', api_key='kyiv_client', check_type='client', point_id= 1)
            Printer.objects.create(name='Kyiv', api_key='kyiv_kitchen', check_type='kitchen', point_id= 1)
            Printer.objects.create(name='Odesa', api_key='odesa_client', check_type='client', point_id= 2)
            Printer.objects.create(name='Odesa', api_key='odesa_kitchen', check_type='kitchen', point_id= 2)
            # Printer.objects.create(name='Lviv', api_key='lviv_client', check_type='client', point_id= 3)
            # Printer.objects.create(name='Lviv', api_key='lviv_kitchen', check_type='kitchen', point_id= 3)
    return

def validate_printer(point):
    printers = Printer.objects.all().filter(point_id = point)
    if len(printers) == 0:
        raise BadRequest('Point doesnt have printers.')
        
