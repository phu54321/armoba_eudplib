import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

from eudplib import *

LoadMap('outputmap/basemap/grpbasemap.scx')


@EUDFunc
def main():
    grp = EUDGrp('outputmap/basemap/inputgrp.grp')
    BasicTrigger(
        actions=SetMemory(0x51CED0 + 4 * 54, SetTo, grp),
        preserved=False
    )


SaveMap('outputmap/testgrp.scx', main)

