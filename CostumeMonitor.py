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
        self.__current_sampling = 0
        self.__current_bytes_sent = 0
        self.__current_bytes_recv = 0

        self.sampling_long = 60  # 60 seconds
        self.__last_min_sampling = [0] * 60

    def check_if_interface_name_exsist(self, interface_name_arg):
        interfaces = psutil.net_io_counters(pernic=True)
        for interface in interfaces:
            interface_name = interface.replace('\u200f', '')
            if interface_name_arg == interface_name:
                self.interface_name = interface
        raise Exception(f"cannot find this interface : {interface_name_arg}")

    def get_current_interface(self):
        return psutil.net_io_counters(pernic=True)[self.interface_name]

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
        return round(value * 8, 2), f'{power_labels[n]}bps'

    def update_sampling(self, bytes_send, bytes_recv):
        self.__current_bytes_sent = bytes_send
        self.__current_bytes_recv = bytes_recv
        self.__current_sampling = self.__current_bytes_sent + self.__current_bytes_recv
        self.__last_min_sampling.insert(0, self.__current_sampling)
        if (len(self.__last_min_sampling) >= self.sampling_long):
            self.__last_min_sampling.pop(self.sampling_long)
        # value, format = self.format_bytes(current_value)

    def check_network_values(self):
        if psutil.net_if_stats()[self.interface_name].isup == False:
            Notifier.send_notfication(f"your interface network is DOWN\n\t: interface name: {self.interface_name}")
        if self.__current_sampling < self.min_value:
            Notifier.send_notfication(
                f"your bandwith is low\n\t current bandwith: {self.format_bytes(self.__current_sampling)}")
        if self.__current_sampling > self.max_value:
            Notifier.send_notfication(
                f"your bandwith is high\n\t: current bandwith: {self.format_bytes(self.__current_sampling)}")

    def get_sampling_info(self):
        low = ' '.join(map(str,self.format_bytes(self.min_value)))
        high = ' '.join(map(str,self.format_bytes(self.max_value)))
        return {'LastMinSampling': self.__last_min_sampling,
                'Low': low,
                'High': high}

    def get_current_sampling(self):
        return {'bytes_sent': self.__current_bytes_sent,
                'bytes_recv': self.__current_bytes_recv,
                'current_bytes': self.__current_sampling}
