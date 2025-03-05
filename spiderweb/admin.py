from django.contrib import admin

from spiderweb.models import Monitor_Status, Monitor_Type, Device_Type, Monitor_Device_List


@admin.register(Monitor_Status)
class Monitor_StatusAdmin(admin.ModelAdmin):
    list_display = ('status_code', 'desc')


@admin.register(Monitor_Type)
class Monitor_TypeAdmin(admin.ModelAdmin):
    list_display = ('type_name', )


@admin.register(Device_Type)
class Device_TypeAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'job_frequency')


@admin.register(Monitor_Device_List)
class Monitor_Device_ListAdmin(admin.ModelAdmin):
    list_display = ('monitor_type', 'device_type', 'device_name', 'ip_address', 'port', 'plant', 'enable', 'status')