from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.conf import settings


class Monitor_Status(models.Model):
    status_code = models.CharField(max_length=3, unique=True, primary_key=True)
    desc = models.CharField(max_length=200, null=False, blank=False)
    ref_url = models.CharField(max_length=500, null=True, blank=True)
    update_at = models.DateTimeField(default=timezone.now)
    update_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                  related_name='check_status_update_by')

    def __str__(self):
        return self.status_code


class Monitor_Type(models.Model):
    type_name = models.CharField(max_length=100, unique=True)
    update_at = models.DateTimeField(default=timezone.now)
    update_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                  related_name='monitor_type_update_by')

    def __str__(self):
        return self.type_name


class Device_Type(models.Model):
    type_name = models.CharField(max_length=100, unique=True)
    job_frequency = models.CharField(max_length=10, null=False, blank=False)
    update_at = models.DateTimeField(default=timezone.now)
    update_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                  related_name='device_type_update_by')

    def __str__(self):
        return self.type_name


class Monitor_Device_List(models.Model):
    monitor_type = models.ForeignKey(Monitor_Type, related_name='monitor_list_monitor_type', on_delete=models.CASCADE, null=False,
                              blank=False)
    device_type = models.ForeignKey(Device_Type, related_name='monitor_list_device_type', on_delete=models.CASCADE, null=False,
                              blank=False)
    device_group = models.CharField(max_length=100, null=True, blank=True)
    device_name = models.CharField(max_length=100, null=False, blank=False)
    ip_address = models.CharField(max_length=50, null=True, blank=True)
    port = models.CharField(max_length=100, null=True, blank=True)
    plant = models.CharField(max_length=50, null=True, blank=True)
    enable = models.CharField(max_length=1, null=False, blank=False, default='Y')
    stop_before = models.CharField(max_length=20, null=True, blank=True)
    status = models.ForeignKey(Monitor_Status, related_name='monitor_list_status', on_delete=models.DO_NOTHING, null=True,
                              blank=True)
    status_update_at = models.DateTimeField(default=timezone.now)
    comment = models.CharField(max_length=500, null=True, blank=True)
    attr1 = models.CharField(max_length=500, null=True, blank=True)
    attr2 = models.CharField(max_length=500, null=True, blank=True)
    attr3 = models.CharField(max_length=500, null=True, blank=True)
    attr4 = models.CharField(max_length=500, null=True, blank=True)
    attr5 = models.CharField(max_length=500, null=True, blank=True)
    update_at = models.DateTimeField(default=timezone.now)
    update_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                  related_name='monitor_list_update_by')

    def __str__(self):
        return self.device_name

class Monitor_Device_Log(models.Model):
    func_name = models.CharField(max_length=50, null=False, blank=False)
    device = models.ForeignKey(Monitor_Device_List, related_name='log_device', on_delete=models.CASCADE, null=False, blank=False)
    status_code = models.ForeignKey(Monitor_Status, related_name='check_log_status', on_delete=models.DO_NOTHING,
                                    null=False, blank=False)
    comment = models.CharField(max_length=200, null=False, blank=False)
    update_at = models.DateTimeField(default=timezone.now)
    notice_flag = models.BooleanField(null=True, blank=True)
    recover_msg = models.BooleanField(null=True, blank=True)
