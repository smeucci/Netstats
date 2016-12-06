import threading
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
    return '{0:.0f}'.format(dl)

def wifi_quality(interface='wlan0'):
    output = subprocess.Popen(['iwconfig', interface], stdout=subprocess.PIPE)
    i = 0
    for line in iter(output.stdout.readline, ''):
        if 'Signal level' in line:
            return parse_wifi_quality(line.rstrip())
        i += 1

def parse_wifi_quality(string):
    string = string.split()
    link_quality = parse_link_quality(string[1].replace('Quality=', ''))
    signal_level = string[3].replace('level=', '')
    return (link_quality, signal_level)

def parse_link_quality(string):
    string = string.split('/')
    return '{0:.0f}'.format(float(string[0]) / float(string[1]) * 100)
