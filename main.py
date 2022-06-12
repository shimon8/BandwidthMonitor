import getopt
import sys
import threading
import time
import psutil
from flask import Flask, jsonify
from CostumeMonitor import CostumeMonitor

app = Flask(__name__)


def init_montioring(*arg):
    argv=arg
    min_value = None
    max_value = None
    interface_name = 'Wi-Fi'  # default

    # parse the arguments
    try:
        opts, args = getopt.getopt(argv[1:],
                                   "s:l:i:",
                                   ["min_value =", "max_value =", "help", "interface_name ="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    # Deal with the arguments
    for opt, arg in opts:

        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ['-s', '--min_value ']:
            min_value = makeInt(arg)
            if min_value < 0:
                print("minimum value cannot be negative number")
                usage()
                sys.exit(2)
        elif opt in ['-l', '--max_value ']:
            max_value = makeInt(arg)
            if max_value < 0:
                print("maximum value cannot be negative number")
                usage()
                sys.exit(2)
        elif opt in ("-i", "--interface_name"):
            interface_name = arg
    if min_value is None or max_value == None:
        usage()
        sys.exit(2)
    if min_value > max_value:
        print("minimum value cannot be bigger than maximum parameter")
        usage()
        sys.exit(2)
    interface_name = check_if_interface_name_exsist(interface_name)
    costume_monitor = CostumeMonitor(interface_name=interface_name, min_value=min_value, max_value=max_value)
    start_monitoring(costume_monitor)


def start_monitoring(costume_monitor):
    old_value = 0

    while True:
        new_value = costume_monitor.get_bandwidh_value()
        if old_value:
            current_value = new_value - old_value
            costume_monitor.send_state(current_value)
            costume_monitor.check_network_values(current_value)

        old_value = new_value
        time.sleep(1)


def usage():
    print("Usage: " + sys.argv[0] + " [options] <host>")
    print
    print("Mandatory arguments to long options are mandatory for short options too")
    print("  -h    --help                         display this help and exit")
    print("  -s    --min_value                    minimum limit  for network bandwidth(by bytes)")
    print("  -l    --max_value                    maximum limit  for network bandwidth(by bytes)")
    print("  -i    --interface_name               interface name for monitoring, Default=Wi-Fi")


def makeInt(value):
    try:
        return int(value)
    except:
        print("An incorrect value was passed in. Aborting!")
        print
        usage()
        sys.exit(2)


def check_if_interface_name_exsist(interface_name_arg):
    interfaces = psutil.net_io_counters(pernic=True)
    for interface in interfaces:
        interface_name = interface.replace('\u200f', '')
        if interface_name_arg == interface_name:
            return interface
    print("cannot find the interface name!")
    usage()
    sys.exit(2)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/getMonitor")
def get():
    return jsonify("costume_monitor")


if __name__ == '__main__':
    # interface_name = check_if_interface_name_exsist("Wi-Fi")
    # costume_monitor = CostumeMonitor(interface_name=interface_name, min_value=1000, max_value=100000000)
    # start_monitoring(costume_monitor)
    montioring = threading.Thread(target=init_montioring, name="Monitor", args=sys.argv)
    montioring.start()
    app.run()

