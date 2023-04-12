from django.apps import AppConfig
import threading
import subprocess
import sys


class Mtp038BackendConfig(AppConfig):
    """
    Configuration for the MTP_038_backend Django app.

    This configuration class defines the app's name and default auto field.
    It also sets up a ready event and a stop event, and starts the
    MyThread thread when the app is ready.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MTP_038_backend'

    # Create a ready event
    ready_event = threading.Event()

    # Create a stop event
    stop_event = threading.Event()

    def ready(self):
        """
        Perform app-specific actions when the app is ready.

        This method sets the ready event and starts the MyThread thread.
        """
        # Check if the current process is running Django test command
        running_tests = 'test' in sys.argv

        if not running_tests:
            # Set the ready event
            self.__class__.ready_event.set()

            # Start the script in a new thread
            print("Starting script...")
            thread = MyThread(self.__class__.stop_event)
            thread.start()


class MyThread(threading.Thread):
    """
    Custom thread class for running the api_stream.py script.

    This class extends the threading.Thread class and overrides the run
    method to execute the api_stream.py script in a separate thread.
    """
    def __init__(self, stop_event):
        super().__init__()
        self.stop_event = stop_event

    def run(self):
        """
        Execute the api_stream.py script in a separate thread.

        This method runs the api_stream.py script using subprocess.run and
        handles any CalledProcessError exceptions that may occur.
        """
        try:
            print("Starting script...")
            # Start the api_stream.py script
            subprocess.run([sys.executable, 'MTP_038_backend/api_stream.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Script finished with error: {e}")

        print("Script finished")