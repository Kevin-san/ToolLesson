#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import alvintools

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PdfWeb.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if alvintools.get_system_name() == "Windows":
        execute_from_command_line(['manage.py','runserver_plus','--cert','server.crt','0.0.0.0:8000'])
    else:
        execute_from_command_line(['manage.py','runserver_plus','0.0.0.0:8000'])


if __name__ == '__main__':
    
    main()
