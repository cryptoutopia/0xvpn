from django.contrib import admin
from bitvpn.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    fields = ('ip', 'expiration', 'access_path')
    list_display = ('ip', 'expiration', 'is_expired')
    date_hierarchy = 'expiration'
