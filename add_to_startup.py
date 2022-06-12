import os
import getpass


def add_to_startup_windows(min_value, max_value, interface=None):
    USER_NAME = getpass.getuser()
    file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = rf'C:\Users\{USER_NAME}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        if interface == None:
            bat_file.write(rf'start "" "{file_path}\main.py" -s {min_value} -l {max_value}')
        else:
            bat_file.write(rf'start "" "{file_path}\main.py" -s {min_value} -l {max_value} -i {interface}')


def add_to_startup_linux(min_value, max_value, interface=None):
    pass
    # TODO


add_to_startup_windows(0, 10000000)
