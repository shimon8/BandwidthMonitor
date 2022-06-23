import os
import threading

import time
from win10toast import ToastNotifier

class Notifier:
    lock = threading.Lock()
    notifier = ToastNotifier()
    waiting_after_notification = 1
    title = "Network Bandwidth Alert"
    icon_path = rf'{os.path.dirname(os.path.realpath(__file__))}\assets\network.ico'

    @staticmethod
    def send_notfication(desc):
        try:
            Notifier.lock.acquire()
            Notifier.notifier.show_toast("Network Bandwidth Alert", desc, icon_path=Notifier.icon_path, duration=2)
        except:
            print("error?")
        finally:
            Notifier.lock.release()
            time.sleep(Notifier.waiting_after_notification)
