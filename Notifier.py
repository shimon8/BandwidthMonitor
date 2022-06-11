from pynotifier import Notification
class Notifier:
    @staticmethod
    def send_notfication(desc):
        Notification(
            title='network notificatin',
            icon_path=r"C:\Users\shimo\Downloads\Symbol_WLAN3_icon-icons.com_55244.ico",
            # On Windows .ico is required, on Linux - .png
            description=desc,
            duration=5,  # Duration in seconds
            urgency='normal'
        ).send()
