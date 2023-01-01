#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
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
"""

import struct
from collections.abc import Iterable
from typing import TYPE_CHECKING, Literal, TypeAlias, overload

from eudplib import utils as ut
from eudplib.localize import _

from ..allocator import IsConstExpr
from ..eudobj import Db, EUDObject
from .action import Action
from .condition import Condition
from .triggerscope import NextTrigger, _RegisterTrigger

if TYPE_CHECKING:
    from ..allocator import Forward
    from ..allocator.payload import RlocInt_C, _PayloadBuffer

# Trigger counter thing

_trgCounter = 0


def GetTriggerCounter() -> int:
    return _trgCounter


# Aux


def _bool2Cond(x: bool | Condition) -> Condition:
    if x is True:
        return Condition(0, 0, 0, 0, 0, 22, 0, 0)  # Always
    elif x is False:
        return Condition(0, 0, 0, 0, 0, 23, 0, 0)  # Never
    else:
        return x


def Disabled(arg: Condition | Action) -> None:
    """Disable condition or action"""
    arg.Disabled()


# RawTrigger
_Trigger: TypeAlias = "RawTrigger | Forward | int | None"
_Condition: TypeAlias = Condition | bool | Iterable[Condition | bool | Iterable] | None
_Action: TypeAlias = Action | Iterable[Action | Iterable] | None


class RawTrigger(EUDObject):
    @overload
    def __init__(
        self,
        prevptr: _Trigger = None,
        nextptr: _Trigger = None,
        conditions: _Condition = None,
        actions: _Action = None,
        *,
        preserved: bool = True,
        currentAction: int | None = None,
        trigSection: None = None
    ) -> None:
        ...

    @overload
    def __init__(
        self,
        prevptr: _Trigger = None,
        nextptr: _Trigger = None,
        conditions: None = None,
        actions: None = None,
        *,
        preserved: Literal[True] = True,
        currentAction: None = None,
        trigSection: bytes
    ) -> None:
        ...

    def __init__(
        self,
        prevptr: _Trigger = None,
        nextptr: _Trigger = None,
        conditions: _Condition = None,
        actions: _Action = None,
        *,
        preserved: bool = True,
        currentAction: int | None = None,
        trigSection: bytes | None = None
    ) -> None:
        super().__init__()

        # Register trigger to global table
        global _trgCounter
        _trgCounter += 1
        _RegisterTrigger(self)  # This should be called before (1)

        # Set linked list pointers
        if prevptr is None:
            prevptr = 0
        if nextptr is None:
            nextptr = NextTrigger()  # (1)
        else:
            ut.ep_assert(IsConstExpr(nextptr), _("nextptr should be ConstExpr"))

        self._prevptr = prevptr
        self._nextptr = nextptr

        # Uses normal condition/action initialization
        if trigSection is None:
            # Normalize conditions/actions
            if conditions is None:
                conditions = []
            conditions = ut.FlattenList(conditions)
            _conditions: list[Condition] = list(map(_bool2Cond, conditions))

            if actions is None:
                actions = []
            actions = ut.FlattenList(actions)

            ut.ep_assert(len(_conditions) <= 16, _("Too many conditions"))
            ut.ep_assert(len(actions) <= 64, _("Too many actions"))

            # Register condition/actions to trigger
            for i, cond in enumerate(_conditions):
                cond.CheckArgs(i)
                cond.SetParentTrigger(self, i)

            for i, act in enumerate(actions):
                act.CheckArgs(i)
                act.SetParentTrigger(self, i)

            self._conditions = _conditions
            self._actions = actions
            self._flags = 4 if preserved else 0
            self._currentAction = currentAction
            if currentAction is not None:
                self._flags |= 1

        # Uses trigger segment for initialization
        # NOTE : player information is lost inside eudplib.
        else:
            self._conditions, self._actions = [], []
            for i in range(16):
                condtype = trigSection[i * 20 + 15]
                if condtype == 22:
                    continue  # ignore Always, no worry disable/enable
                elif condtype >= 1:
                    self._conditions.append(
                        Condition(*struct.unpack_from("<IIIHBBBBH", trigSection, i * 20))
                    )
            self._flags = trigSection[320 + 2048] & 5
            for i in range(64):
                acttype = trigSection[320 + i * 32 + 26]
                if acttype == 47:  # Comment
                    continue
                elif acttype >= 1:
                    self._actions.append(
                        Action(*struct.unpack_from("<IIIIIIHBBBBH", trigSection, 320 + i * 32))
                    )
            self._currentAction = None if not (self._flags & 1) else trigSection[2399]

    @property
    def preserved(self) -> bool:
        return bool(self._flags & 4)

    @preserved.setter
    def preserved(self, preserved: bool) -> None:
        if preserved:
            self._flags |= 4
        else:
            self._flags &= ~4

    def GetDataSize(self) -> int:
        return 2408

    def CollectDependency(self, pbuffer: "_PayloadBuffer") -> None:
        pbuffer.WriteDword(self._prevptr)
        pbuffer.WriteDword(self._nextptr)

        for cond in self._conditions:
            cond.CollectDependency(pbuffer)
        for act in self._actions:
            act.CollectDependency(pbuffer)

    def WritePayload(self, pbuffer: "_PayloadBuffer") -> None:
        pbuffer.WriteDword(self._prevptr)
        pbuffer.WriteDword(self._nextptr)

        # Conditions
        for cond in self._conditions:
            cond.WritePayload(pbuffer)

        if len(self._conditions) != 16:
            pbuffer.WriteBytes(bytes(20))
            pbuffer.WriteSpace(20 * (15 - len(self._conditions)))

        # Actions
        for act in self._actions:
            act.WritePayload(pbuffer)

        if len(self._actions) != 64:
            pbuffer.WriteBytes(bytes(32))
            pbuffer.WriteSpace(32 * (63 - len(self._actions)))

        # Preserved flag
        pbuffer.WriteDword(self._flags)

        pbuffer.WriteSpace(27)
        if self._currentAction is None:
            pbuffer.WriteByte(0)
        else:
            pbuffer.WriteByte(self._currentAction)
