import threading
from collections import deque
import time
import psutil
import subprocess

def bytes_received(interface='wlan0'):
    t0 = time.time()
    counter = psutil.net_io_counters(pernic=True)[interface]
    return (t0, counter.bytes_recv)

def download_speed(first, second):
    t0, first = first
    t1, second = second
    # compute download speed
    dl = (second - first) / (t1 - t0) / 1000.0
    return "{0:.0f}".format(dl)

def signal_level(interface='wlan0'):
    output = subprocess.Popen(['iwconfig', interface], stdout=subprocess.PIPE)
    i = 0
    for line in iter(output.stdout.readline, ''):
        if (i == 5):
            print line.rstrip()
        i += 1
