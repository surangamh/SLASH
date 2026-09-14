# Copyright (C) 2025 Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

import argparse
import time
from dcmac_init import dcmac_logic_init
from dcmac_mmio import DCMAC
from utils import add_common_args, get_ip_offset
from udp_utils import NetworkLayer
from trafficgen import TrafficGenerator

"""This file aims at doing a test of the Ethernet or UDP layer between two interfaces in
board, interface 0 and 2. It will initialize the DCMAC and then setup the
interfaces IP, MAC addresses as well as the UDP socket table.
"""

DCMAC_BASEADDR = 0x200_0000
TRAFFICGEN_BASEADDR = 0x400_2000
#NL_BASEADDR = 0x400_0000


class ArgsClass:
    dcmac = 0
    init = False
    print = 1
    dev = 0
    verbose = 1
    loopback = 1
    keep_alive = 0
    align_rx = 1
    traffic_test = 1


def main(args):
    """Initialize DCMAC in each interface"""
    init_args = ArgsClass()
    init_args.dev = args.dev
    """Init DCMAC 0"""
    dcmac_logic_init(init_args)

    tgen0 = TrafficGenerator(args.dev, resource=0, base_offset=0x004C_0000)

    tgen0.flits = 22
    tgen0.dest = 0
    tgen0.start()
    time.sleep(1)

    dcmac0 = DCMAC(args.dev, base_offset=get_ip_offset(DCMAC_BASEADDR, 0))
    print(f'{dcmac0.tx_stats(verbose=1)=}')
    print(f'{dcmac0.rx_stats(verbose=1)=}')



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--udp', action='store_true',
                        help='Use UDP logic')
    parser = add_common_args(parser, verbose=True)
    args = parser.parse_args()
    main(args)
