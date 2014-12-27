#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Copyright (c) 2014 trgk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

from .. import core as c
from .filler import filldw, fillwbb, fillbbbb

def HasEUDVariable(l):
    for i in l:
        if isinstance(i, c.EUDVariable):
            return True
    return False

def ApplyPatchTable(initepd, obj, patchtable):
    for i, pt in enumerate(patchtable):
        attrs = patchtable
        filler = {
            'd':1,
            'wbb':3,
            'bbbb':4
        }[len(attrs)]
        attrs = c.Assignable2List(attrs)

        vars = [getattr(obj, attr) if type(attr) is str else attr for attr in attrs]
        if HasEUDVariable(vars):
            filler(initepd + i, *vars)
            for attr in attrs:
                if type(attr) is str:
                    setattr(obj, attr, 0)

condpt = [
    ['locid'],
    ['player'],
    ['amount'],
    ['unitid', 'comparison', 'condtype'],
    ['restype', 'flags', 0, 0],
]

actpt = [
    ['locid1'],
    ['strid'],
    ['wavid'],
    ['time'],
    ['player1'],
    ['player2'],
    ['unitid', 'acttype', 'amount'],
    ['flags', 0, 0, 0]
]

# TODO : test this function
class Trigger(c.Expr):
    def __init__(
        self,
        conditions=None,
        actions=None,
        preserved=True
    ):
        super().__init__()
        if conditions is None:
            conditions = []
        if actions is None:
            actions = []
        conditions = c.FlattenList(conditions)
        actions = c.FlattenList(actions)

        triggerstart = c.NextTrigger()
        trg = c.Forward()

        # conditions
        for i, cond in enumerate(conditions):
            ApplyPatchTable(c.EPD(trg + 8 + 20 * i), cond, condpt)

        # actions
        for i, act in enumerate(actions):
            ApplyPatchTable(c.EPD(trg + 328 + 32 * i), act, actpt)

        trg << c.BasicTrigger(
            conditions=conditions,
            actions=actions,
            preserved=preserved
        )

        self.tstart = triggerstart
        self.tmain = trg

    def Evaluate(self):
        return c.Evaluate(self.tstart)

    def GetNextPtrMemory(self):
        return self.tmain + 4

