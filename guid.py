#!/usr/local/bin/python3
import time
import sys
import random
import struct
from datetime import datetime

# This is a Python replacement for the guid.php file that comes with suiteCRM. This is meant to be
# used as a module, called with "import guid", and referenced with "guid.result".
# Created by: Nathan LeSueur


def rand_num(num):
    result = ""
    for x in range(0, num):
        x = random.randint(0, 15)
        hex_num = "%x" % x
        result += hex_num
    return result


def float_to_hex(f):
    x = (struct.unpack('<I', struct.pack('<f', f))[0])
    return "%x" % x

def get_id():
    dt = datetime.now()
    ms = (dt.microsecond / 1000000.)
    etime = int(time.time())

    hex_epoch = "%x" % etime
    hex_ms = (float_to_hex(ms))

    result = (str(hex_ms[:5]) + rand_num(3) + "-" + rand_num(4) + "-" +
          rand_num(4) + "-" + rand_num(4) + "-" + str(hex_epoch[:6]) + rand_num(6))
    return result
if __name__ == "__main__":
    print(get_id())
