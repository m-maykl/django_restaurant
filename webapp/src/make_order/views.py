import os
from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from make_order.tasks import write_html
from make_order.forms import Order_form
from make_order.models import Printer, Check
from make_order.utils import validate_printer, add_printers




orders_list = {'burger': 'Бургер', 'roll': 'Ролл', 'salad': 'Салат', 'coca_cola': 'Coca-Cola', 'ice_cream': 'Морозиво'}
points_list = {'1':'Київ', '2':'Одеса', '3':'Львів'}

def make_order_view(request):
    add_printers()
    form = Order_form()
    if request.method == "POST":
        value = Order_form(request.POST)
        if value.is_valid():
            order = []
            resp = request.POST
            point = resp.get('point')
            validate_printer(point)
            for i in resp:
                for k, v in orders_list.items():
                    if i == k:
                        order.append(v)
            if order != []:
                printers = Printer.objects.all().filter(point_id = point)
                num_checks = len(Check.objects.all())
                if num_checks == 0:
                    order_id = 1
                else:
                    order_id = int((num_checks / 2) + 1)
                for printer in printers:
                    Check.objects.create(printer_id= printer, type= printer.check_type, order= order, status = 'new')
                    check = Check.objects.filter(status = 'new').latest('id')
                    write_html.delay({'id': check.id, 'point': points_list.get(point), 'order': order, 'order_num': order_id})
    return render(request, "make_order.html", context = {'form':form})


def show_pdf(request, name_pdf):
    filepath = os.path.join('/app/src/media/pdf/', name_pdf)
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
    
