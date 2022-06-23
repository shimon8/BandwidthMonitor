import os
import getpass


def add_to_startup_windows(min_value, max_value, interface=None):
    USER_NAME = getpass.getuser()
    file_path = os.path.dirname(os.path.realpath(__file__))
    pyton_path = rf'{file_path}\venv\Scripts\python.exe'
    bat_path = rf'C:\Users\{USER_NAME}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        if interface == None:
            bat_file.write(rf'{pyton_path} "{file_path}\main.py" -l {min_value} -h {max_value}')
        else:
            bat_file.write(rf'{pyton_path} "{file_path}\main.py" -l {min_value} -h {max_value} -i {interface}')


def add_to_startup_linux(min_value, max_value, interface=None):
    pass
    # TODO


min_value = 0
max_value = 100000
interface = None
add_to_startup_windows(min_value, max_value, interface)
