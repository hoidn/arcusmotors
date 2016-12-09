#!/bin/sh
sudo install arcus.rules /lib/udev/rules.d
sudo udevadm control --reload-rules
