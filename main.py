import getopt
import sys
import threading
import time

import flask
import psutil
from CostumeMonitor import CostumeMonitor
from flask import Flask
from flask_cors import CORS

DELAY_SAMPLING = 1


# region init Monitoring
def init_montioring(args):
    argv = args
    min_value = None
    max_value = None
    interface_name = 'Wi-Fi'  # default
    # parse the arguments
    try:
        opts, args = getopt.getopt(argv[1:],
                                   "l:h:i:",
                                   ["min_value =", "max_value =", "help", "interface_name ="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    # Deal with the arguments
    for opt, arg in opts:
        if opt == "--help":
            usage()
            sys.exit()
        elif opt in ['-l', '--low ']:
            min_value = makeInt(arg)
            if min_value < 0:
                print("minimum value cannot be negative number")
                usage()
                sys.exit(2)
        elif opt in ['-h', '--high ']:
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
    io = costume_monitor.get_current_interface()
    while True:
        time.sleep(DELAY_SAMPLING)
        io_2 = costume_monitor.get_current_interface()
        send_bytes = io_2.bytes_sent - io.bytes_sent
        recv_bytes = io_2.bytes_recv - io.bytes_recv
        costume_monitor.update_sampling(send_bytes,recv_bytes)
        costume_monitor.check_network_values()
        io=io_2

def usage():
    print("        --help                   display this help and exit")
    print("  -l    --low                    low  limit  for network bandwidth(by bytes)")
    print("  -h    --high                   high limit  for network bandwidth(by bytes)")
    print("  -i    --interface_name         interface name for monitoring, Default=Wi-Fi")


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
    response = flask.jsonify(costume_monitor.get_current_sampling())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getSamplingInfo')
def get_sampling_info():
    response = flask.jsonify(costume_monitor.get_sampling_info())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
# endregion


if __name__ == '__main__':
    costume_monitor = init_montioring(sys.argv)
    montioring = threading.Thread(target=start_monitoring, name="Monitor")
    montioring.start()

    app.run(debug=True)
