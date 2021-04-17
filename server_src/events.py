# Interupt handling
from signal import signal, SIGINT
import sys
import threading

exit_event = threading.Event()

def signal_handler(_signum, _frame):
    if not signal_handler.SECOND_INT:
        signal_handler.SECOND_INT = True
        print("Graceful exit. Waiting for socket to close..." )
        exit_event.set()

    else:
        print("Hard exit")
        sys.exit(1)

signal_handler.SECOND_INT = False

signal(SIGINT, signal_handler)
