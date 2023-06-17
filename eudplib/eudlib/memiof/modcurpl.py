#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2014 by trgk.
# All rights reserved.
# This file is part of EUD python library (eudplib), and is released under "MIT License Agreement".
# Please see the LICENSE file that should have been included as part of this package.

import random

from eudplib import core as c
from eudplib import ctrlstru as cs
from eudplib import utils as ut
from eudplib.eudlib.s import SetMemoryC


def f_setcurpl(cp, *, actions=[], set_modifier=True):
    if c.IsEUDVariable(cp):
        cpcond = c.curpl.cpcacheMatchCond()
        cpcache = c.curpl.GetCPCache()
        c.VProc(
            cp,
            actions + cp.QueueAssignTo(cpcache) if set_modifier else [cp.SetDest(cpcache)],
        )
        c.VProc(
            [cp, cpcache],
            [cp.SetDest(ut.EPD(cpcond) + 2), cpcache.SetDest(ut.EPD(0x6509B0))],
        )
    else:
        cs.DoActions(c.SetCurrentPlayer(cp))


def f_setcurpl2cpcache(v=[], actions=[]):
    cpcache = c.curpl.GetCPCache()
    if v:
        trg = c.VProc([v] + [cpcache], [actions] + [cpcache.SetDest(ut.EPD(0x6509B0))])
    else:
        trg = c.VProc(cpcache, [actions] + [cpcache.SetDest(ut.EPD(0x6509B0))])

    return trg


# This function initializes _curpl_checkcond, so should be called at least once
@c.EUDFunc
def _f_updatecpcache():
    cpcond = c.curpl.cpcacheMatchCond()
    cpcache = c.curpl.GetCPCache()
    c.RawTrigger(
        actions=[
            SetMemoryC(cpcache.getValueAddr(), c.SetTo, 0),
            SetMemoryC(cpcond + 8, c.SetTo, 0),
        ]
    )
    for i in ut.RandList(range(32)):
        u = random.randint(234, 65535)
        c.RawTrigger(
            conditions=c.DeathsX(ut.EPD(0x6509B0) - 12 * u, c.AtLeast, 1, u, 2**i),
            actions=[
                SetMemoryC(cpcache.getValueAddr(), c.Add, 2**i),
                SetMemoryC(cpcond + 8, c.Add, 2**i),
            ],
        )


@c.EUDFunc
def f_getcurpl():
    """Get current player value.

    eudplib internally caches the current player value, so this function uses
    that value if the value is valid. Otherwise, update the current player
    cache and return it.
    """
    cpcond = c.curpl.cpcacheMatchCond()
    cpcache = c.curpl.GetCPCache()
    f_getcurpl._frets = [cpcache]
    f_getcurpl._retn = 1
    f_getcurpl._fend << cpcache.GetVTable()
    f_getcurpl._nptr = cpcache.GetVTable() + 4
    if cs.EUDIfNot()(cpcond):
        _f_updatecpcache()
    cs.EUDEndIf()

    c.SetNextTrigger(cpcache.GetVTable())
    # return cpcache  # its dest can vary


def f_addcurpl(cp):
    """Add current player value.

    eudplib internally caches the current player value,
    so this function add to that value.
    """
    if c.IsEUDVariable(cp):
        cpcond = c.curpl.cpcacheMatchCond()
        cpcache = c.curpl.GetCPCache()
        c.VProc(cp, cp.QueueAddTo(cpcache))
        c.VProc(cp, cp.SetDest(ut.EPD(cpcond) + 2))
        c.VProc(cp, cp.SetDest(ut.EPD(0x6509B0)))
    else:
        cs.DoActions(c.AddCurrentPlayer(cp))


c.PushTriggerScope()
f_getcurpl()  # Force initialize f_getcurpl
c.PopTriggerScope()
