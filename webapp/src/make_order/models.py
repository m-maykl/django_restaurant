from django.db import models

# Create your models here.
class Printer(models.Model):
    name = models.CharField(max_length=80)
    api_key = models.CharField(max_length=80)
    check_type = models.CharField(max_length=80)
    point_id = models.IntegerField()

    def __str__(self):
        return self.api_key


class Check(models.Model):
    printer_id = models.ForeignKey(Printer, models.PROTECT)
    type = models.CharField(max_length=80)
    order = models.JSONField()
    status = models.CharField(max_length=80)
    pdf_file = models.FileField()
    
    def __str__(self):
        return '{} {} {} {} {} {}'.format(self.id, self.printer_id, self.type, self.order, self.status, self.pdf_file)
