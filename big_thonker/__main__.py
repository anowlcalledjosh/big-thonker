#!/usr/bin/env python3


import collections
from enum import Enum
from pathlib import Path
import subprocess
import threading

import gi

gi.require_version("Gtk", "3.0")

from gi.repository import GLib, Gtk
import indicator_applet
import psutil


class ThonkApplet(indicator_applet.Applet):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.items = collections.OrderedDict(
            status=Gtk.MenuItem("CPU usage:"),
            sep=Gtk.SeparatorMenuItem(),
            quit=Gtk.MenuItem("Quit"),
        )
        self.items["status"].set_sensitive(False)
        self.lock = threading.RLock()

    def schedule_update(self) -> None:
        with self.lock:
            usage = psutil.cpu_percent()
            GLib.idle_add(self.do_update, usage)

    def do_update(self, usage: float) -> None:
        super().do_update()
        self.items["status"].set_label(f"CPU usage: {usage}%")
        self.indicator.icon = f"thonk-{round(usage / 20)}"


def main():
    ThonkApplet(
        "thonk-applet",
        "thonk-unknown",
        indicator_applet.Category.HARDWARE,
        Path("/home/ash/src/big-thonker/").resolve().as_posix(),
    ).run()


if __name__ == "__main__":
    main()
