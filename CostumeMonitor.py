from queue import Queue

import psutil
from collections import deque
from Notifier import Notifier


class CostumeMonitor:
    def __init__(self, interface_name, min_value, max_value):
        self.interface_name = interface_name  # interface name for monitoring
        self.min_value = min_value  # min value by bytes
        self.max_value = max_value  # max value by bytes
        self.is_down = False  # interface name for monitoring
        self.current_sampling = 0

        self.sampling_long = 60  # 60 seconds
        self.last_min_sampling = Queue(maxsize=self.sampling_long)  # 60 sec-> every element is sampling on the laste minute

    def check_if_interface_name_exsist(self, interface_name_arg):
        interfaces = psutil.net_io_counters(pernic=True)
        for interface in interfaces:
            interface_name = interface.replace('\u200f', '')
            if interface_name_arg == interface_name:
                self.interface_name = interface
        raise Exception(f"cannot find this interface : {interface_name_arg}")

    def get_bandwidh_value(self):
        current_interface = psutil.net_io_counters(pernic=True)[self.interface_name]
        return current_interface.bytes_sent + current_interface.bytes_recv

    def format_bytes(self, value):
        # 2**10 = 1024
        power = 2 ** 10
        n = 0
        power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while value > power:
            value /= power
            n += 1
        if n == 0:
            value = 0
            n = +1
        return round(value * 8,2), f'{power_labels[n]}bps'

    def update_sampling_list(self, current_value):
        # update graph falue
        self.update_last_min_sampling(current_value)
        #value, format = self.format_bytes(current_value)

    def update_last_min_sampling(self, current_value):
        # self.last_min_sampling[0] = current_value
        # self.last_min_sampling.pop(self.sampling_long-1)
        self.last_min_sampling.put(current_value)
        print(self.get_sampling_as_list())

    def check_network_values(self, current_value):
        if psutil.net_if_stats()[self.interface_name].isup == False:
            Notifier.send_notfication(f"your interface network is DOWN\n\t: interface name: {self.interface_name}")
        if current_value < self.min_value:
            Notifier.send_notfication(f"your bandwith is low\n\t current bandwith: {self.format_bytes(current_value)}")
        if current_value > self.max_value:
            Notifier.send_notfication(f"your bandwith is high\n\t: current bandwith: {self.format_bytes(current_value)}")

    def get_sampling_as_list(self):
        return list(self.last_min_sampling.queue)