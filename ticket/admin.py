from django.contrib import admin
from . import models

class SystemUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'is_staff', 'is_active', 'date_joined')

class SoftwareAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'version')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'status', 'assignee', 'source', 'created_by', 'created_dt', 'updated_by', 'updated_dt')

admin.site.register(models.SystemUser, SystemUserAdmin)
admin.site.register(models.Staff)
admin.site.register(models.Client)
admin.site.register(models.TicketCategory)
admin.site.register(models.Software, SoftwareAdmin)
admin.site.register(models.Ticket, TicketAdmin)
admin.site.register(models.TicketComment)
