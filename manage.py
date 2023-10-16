# """Django's command-line utility for administrative tasks."""
# import os
# import sys
# import subprocess

# def main():
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'classmanager.settings')
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(sys.argv)


# if __name__ == '__main__':
#     main()



"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading

def run_custom_script():
    # Run your custom script here
    os.system("python arduino.py")

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'classmanager.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Create a thread to run the custom script in parallel
    custom_thread = threading.Thread(target=run_custom_script)
    custom_thread.start()
    
    # Start the Django development server
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
