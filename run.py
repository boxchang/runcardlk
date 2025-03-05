import os
import sys
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thickness_device.settings")
    execute_from_command_line(["manage.py", "runserver", "0.0.0.0:10002"])