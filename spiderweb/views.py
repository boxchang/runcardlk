import json
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt

from spiderweb.models import Device_Type, Monitor_Device_List, Monitor_Device_Log, Monitor_Status
from thickness_device.database import vnedc_database


def spiderweb(request):
    device_types = Device_Type.objects.all()
    monitor_list = [device.type_name for device in device_types if device.type_name != 'WECOM']
    monitor_mode = []
    monitor_name = []
    monitor_msg = []
    db = vnedc_database()
    for name in monitor_list:
        filtered_result = []
        # result = Monitor_Device_List.objects.filter(
        #     enable='Y',
        #     device_type__type_name=name,
        # ).select_related('device_type').order_by('device_type__id', 'device_group', 'device_name')
        sql = f"""
        select dlg.id, dt.type_name, dl.status_id, dl.device_name, dlg.comment, s.ref_url,
        max(case when dl.status_id != 'S01' and enable = 'Y' and dlg.recover_msg is NULL and dl.device_type_id = dt.id then dlg.update_at end) as update_at
        from [VNEDC].[dbo].[spiderweb_device_type] dt
        join  [VNEDC].[dbo].[spiderweb_monitor_device_list] dl on dl.device_type_id = dt.id
        join [VNEDC].[dbo].[spiderweb_monitor_device_log] dlg on dlg.func_name = dt.type_name and dlg.device_id = dl.id
		join [VNEDC].[dbo].[spiderweb_monitor_status] s on dl.status_id = s.status_code
        where dl.status_id != 'S01' and enable = 'Y' and dlg.recover_msg is NULL and type_name = '{name}'
        and (GETDATE() > CONVERT(DATETIME, stop_before, 103) or stop_before ='')
        group by dlg.id, dt.type_name, dl.status_id, dl.device_name, dlg.comment,s.ref_url
        """
        result = db.select_sql_dict(sql)
        filtered_result = [fresult for fresult in result if 'E' in fresult['status_id']]
        monitor_mode.append(len(set([str(item['device_name']) for item in filtered_result])))

        if str(name) == 'COUNTING DEVICE' or str(name) == 'AOI DEVICE':
            # monitor_name.append(','.join(sorted(list(set([f"{str(item.device_group).split('_')[-2][:-1]}{str(item.device_group).split('_')[-1][1:]}" for item in filtered_result])))))
            if str(name) == 'COUNTING DEVICE':
                monitor_name.append(','.join(sorted(list(set([str(item) for item in filtered_result])))))
                monitor_msg.append([[item['id'], item['device_name'], item['update_at'], item['comment'], item['ref_url']] for item in filtered_result])
            elif str(name) == 'AOI DEVICE':
                monitor_name.append(','.join(sorted(list(set([str(item) for item in filtered_result])))))
                monitor_msg.append([[item['id'], item['device_name'], item['update_at'], item['comment'], item['ref_url']] for item in filtered_result])
        elif str(name) == 'PLC SCADA':
            monitor_name.append(','.join(sorted(list(set([str(item) for item in filtered_result])))))
            monitor_msg.append([[item['id'], item['device_name'], item['update_at'], item['comment'], item['ref_url']] for item in filtered_result])
        elif str(name) == 'MES DATA':
            monitor_name.append(','.join(sorted(list(set([str(item) for item in filtered_result])))))
            monitor_msg.append([[item['id'], item['device_name'], item['update_at'], item['comment'], item['ref_url']] for item in filtered_result])
        elif str(name) == 'KEY_DEVICE' or str(name) == 'SAPTicket':
            monitor_name.append(','.join(sorted(list(set([str(item) for item in filtered_result])))))
            monitor_msg.append([[item['id'], item['device_name'], item['update_at'], item['comment'], item['ref_url']] for item in filtered_result])

    monitor_web = zip(monitor_list, monitor_mode, monitor_name, monitor_msg)
    job_frequencies = list(Device_Type.objects.values_list('job_frequency', flat=True))
    reload_time = (min(map(int, job_frequencies))*1000)/50
    last_update_time = str((Monitor_Device_List.objects.filter(enable='Y').order_by('-status_update_at').values('status_update_at').first())['status_update_at']).split('.')[0]

    return render(request, 'spiderweb/spiderweb.html', locals())


def abnormal_recover(request, pk):
    issue = get_object_or_404(Monitor_Device_Log, pk=pk)

    device = Monitor_Device_List.objects.get(device_name=issue.device.device_name)
    device.status = Monitor_Status.objects.get(status_code="S01")
    device.save()

    issue.recover_msg = True
    issue.save()
    return redirect(reverse('spiderweb'))


def spiderweb_config(request):

    data = list(Monitor_Device_List.objects.values('device_group', 'device_name', 'update_at', 'update_by', 'enable',
                                                   'stop_before'))

    # Lấy model người dùng tùy chỉnh
    User = get_user_model()

    for monitor_list in data:
        user = User.objects.get(id=monitor_list['update_by'])
        monitor_list['update_by'] = user.username
        monitor_list['update_at'] = monitor_list['update_at'].strftime('%Y-%m-%d %H:%M:%S')
        # Đảm bảo rằng 'enable' là một chuỗi 'Y' hoặc 'N'
        monitor_list['enable'] = 'Y' if monitor_list['enable'] == 'Y' else 'N'
    return JsonResponse({'data': data}, safe=False)


def config_layout(request):

    return render(request, 'spiderweb/spiderweb_config.html')


def toggle_device_status(request):
    if request.method == 'POST':
        device_name = request.POST.get('status')
        is_active = request.POST.get('is_active') == 'true'

        try:
            device = Monitor_Device_List.objects.get(device_name=device_name)
            device.enable = 'Y' if is_active else 'N'
            device.update_at = timezone.now()
            device.update_by = request.user
            device.save()
            return JsonResponse({'message': 'Device status updated successfully'})

        except Monitor_Device_List.DoesNotExist:
            return JsonResponse({'error': 'Device not found'}, status=404)
    return JsonResponse({'message': 'Invalid request'})


def save_datetime(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            device_name = data.get("device_name")
            stop_before = data.get("stop_before")

            device = Monitor_Device_List.objects.get(device_name=device_name)
            device.stop_before = stop_before  # Lưu giá trị chuỗi "d-m-Y H:i"
            device.save()

            return JsonResponse({"message": "Datetime saved successfully!"})
        except Exception as e:
            return JsonResponse({"message": f"Unexpected error: {str(e)}"}, status=500)

    return JsonResponse({"message": "Invalid request method."}, status=400)