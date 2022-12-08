from django.db import models
from datetime import datetime
from django.contrib import admin
from django.utils.html import format_html

class Client(models.Model):
    ip = models.CharField(max_length=255)
    public_key = models.CharField(max_length=255)
    out_interface = models.CharField(max_length=10)
    expiration = models.DateField()

    @admin.display(description='Expired')
    def is_expired(self):
        if datetime.now().date() > self.expiration:
            return format_html('<span style="color: red">Expired</span>')
        return format_html('<span style="color: #8ce605">Active</span>')

class BtcPay(models.Model):
    pickle = models.TextField(primary_key=True)

    class Meta:
        db_table = 'btcpay'

class Wgman(models.Model):
    pickle = models.TextField(primary_key=True)

    class Meta:
        db_table = 'wireguard'

class Vouchers(models.model):
    id = models.BigAutoField(primary_key=True)
    discount = models.PositiveBigIntegerField()
    used = models.PositiveBigIntegerField(default=0)




