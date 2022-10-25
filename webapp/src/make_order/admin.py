from django.contrib import admin
from make_order.models import Check

# Register your models here.

@admin.register(Check)
class ChecksAdmin(admin.ModelAdmin):
    list_display = ['printer_id', 'type', 'order', 'status', 'pdf_file']
    list_filter = ('printer_id','type', 'status')