import getopt
import sys
import threading
import time

import flask
import psutil
from CostumeMonitor import CostumeMonitor
from flask import Flask, jsonify
from flask_cors import CORS


# region init Monitoring
def init_montioring(args):
    argv = args
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
    return CostumeMonitor(interface_name=interface_name, min_value=min_value, max_value=max_value)


def start_monitoring():
    old_value = 0
    while True:
        new_value = costume_monitor.get_bandwidh_value()
        if old_value:
            current_value = new_value - old_value
            costume_monitor.update_sampling_list(current_value)
            costume_monitor.check_network_values(current_value)

        old_value = new_value
        time.sleep(1)


def usage():
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


# endregion


app = Flask(__name__)
CORS(app)


# region route
@app.route('/getLastSampling')
def get_last_sampling():
    response = flask.jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getLastMintueSampling')
def get_last_mintue_sampling():
    response = flask.jsonify({'LastMinSampling': costume_monitor.last_min_sampling})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# endregion


if __name__ == '__main__':
    # interface_name = check_if_interface_name_exsist("Wi-Fi")
    # costume_monitor = CostumeMonitor(interface_name=interface_name, min_value=1000, max_value=100000000)
    # start_monitoring(costume_monitor)
    # # init_montioring(sys.argv)
    # montioring = threading.Thread(target=init_montioring, name="Monitor", args=sys.argv)
    # montioring.start()
    costume_monitor = init_montioring(sys.argv)
    print(costume_monitor)
    montioring = threading.Thread(target=start_monitoring, name="Monitor")
    montioring.start()

    app.run(debug=True)
