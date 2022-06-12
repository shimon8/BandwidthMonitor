from pynotifier import Notification
from win10toast import ToastNotifier


class Notifier:
    @staticmethod
    def send_notfication(desc):
        try:
            notf = ToastNotifier()
            notf.show_toast("Network Bandwidth Alert", desc, "./assets/network.ico")
            # Notification(
            #     title='network notificatin',
            #     icon_path=r"./assets/network.ico",
            #     # On Windows .ico is required, on Linux - .png
            #     description=desc,
            #     duration=5,  # Duration in seconds
            #     urgency='normal'
            # ).send()
        except:
            print("Error", desc)
