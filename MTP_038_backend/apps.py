from django.apps import AppConfig
import threading
import asyncio
import subprocess
import sys


class Mtp038BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MTP_038_backend'

    # Create a ready event
    ready_event = threading.Event()

    def ready(self):
        # Set the ready event
        self.__class__.ready_event.set()

        # Start the script in a new thread
        print("Starting script...")
        thread = MyThread()
        thread.start()


class MyThread(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            subprocess.run([sys.executable, 'MTP_038_backend/api_stream.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Script finished with error: {e}")

        print("Script finished")