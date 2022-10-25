import json
import requests
from celery import shared_task
from base64 import b64encode
from make_order.models import Check
from django.conf import settings

url = 'http://wkhtmltopdf:80/'


@shared_task
def write_html(check):
    html_str = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <link 
        rel="stylesheet"
        href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
    </head>
    <body>
        <center>
            <h4>Замовлення # {check.get('order_num')}</h4>
        <h4>Заклад: {check.get('point')}</h4>
        <h4>Перелік замовлення: { ", ".join(check.get('order'))}</h4>
        </center>
    </body>
    </html>
    """
    html_file= open("/app/src/proj/templates/check_template.html","w")
    html_file.write(html_str)
    html_file.close()
    created_check = Check.objects.get(id = check.get('id'))
    created_check.status = 'rendered'
    created_check.save()
    html_to_pdf(check)
    return


def html_to_pdf(check):
    created_check = Check.objects.get(id = check.get('id'))

    with open('/app/src/proj/templates/check_template.html', 'rb') as open_file:
        byte_content = open_file.read()
    
    base64_bytes = b64encode(byte_content)
    base64_string = base64_bytes.decode('utf-8')
    data = {'contents': base64_string,}
    headers = {'Content-Type': 'application/json',}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    file_name = str(check.get('order_num')) + '_' + str(created_check.type)
    file_path = '/app/src/media/pdf/' + file_name + '.pdf'
    with open(file_path, 'wb') as f:
        f.write(response.content)
    created_check.status = 'printed'
    created_check.pdf_file = file_path
    created_check.save()
    return