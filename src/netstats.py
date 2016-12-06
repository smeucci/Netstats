#!/usr/bin/env python3

import signal
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, AppIndicator3, GObject
import time
from threading import Thread
from stats import *

class WifiIndicator():
    def __init__(self):
        self.app = 'netstats'
        icon = os.path.dirname(os.path.abspath(__file__)) + '/../icon/downup.svg'
        self.indicator = AppIndicator3.Indicator.new(
            self.app, icon,
            AppIndicator3.IndicatorCategory.OTHER
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.menu())
        self.indicator.set_label('| ?? kB/s | ?? dBm | ?? % |', self.app)
        # thread
        self.update = Thread(target=self.stats)
        # daemonize the thread to make the indicator stopable
        self.update.setDaemon(True)
        self.update.start()

    def menu(self):
        menu = Gtk.Menu()
        # menu item
        item = Gtk.MenuItem('Item')
        menu.append(item)
        # separator
        menu.append(Gtk.SeparatorMenuItem())
        #quit
        quit = Gtk.MenuItem('Quit')
        quit.connect('activate', self.stop)
        menu.append(quit)

        menu.show_all()
        return menu

    def stop(self, source):
        Gtk.main_quit()

    def stats(self):
        t = 2
        while True:
            first = bytes_received()
            time.sleep(1)
            second = bytes_received()
            dl = download_speed(first, second)
            qlt, lvl = wifi_quality()
            mention = '| ' + dl +  ' kB/s | ' + lvl + ' dBm' + ' | ' + qlt + ' % |'
            # apply the interface update using GObject.idle_add()
            GObject.idle_add(
                self.indicator.set_label,
                mention, self.app,
                priority=GObject.PRIORITY_DEFAULT
            )
            t += 1


WifiIndicator()
GObject.threads_init
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
