import time
import queue
import sys
from threading import Thread

message_queue = queue.Queue()
keep_running = True


def say(text):
    message_queue.put(text)


if sys.platform == 'win32':
    import pythoncom
    import win32com.client


    def _init():
        pythoncom.CoInitialize()


    def _say(text):
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak(text)
else:
    import subprocess


    def _init():
        pass


    def _say(text):
        subprocess.run(['say', text])


def _process_messages():
    _init()
    while keep_running:
        try:
            text = message_queue.get_nowait()
            _say(text)

        except queue.Empty:
            pass
        time.sleep(0.1)


Thread(target=_process_messages).start()


def shutdown():
    global keep_running
    keep_running = False
