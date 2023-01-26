## NOTE: THIS FILE IS GENERATED BY EPSCRIPT! DO NOT MODITY
from eudplib import *
from eudplib.epscript.helper import _RELIMP, _IGVA, _CGFW, _ARR, _VARR, _SRET, _SV, _ATTW, _ARRW, _ATTC, _ARRC, _L2V, _LVAR, _LSH
# (Line 1) import .BGM_eps_test;
# (Line 2) import .test_eps_stattext as stat;
BGM_eps_test = _RELIMP(".", "BGM_eps_test")
# (Line 3) var x = 1 << 4;
stat = _RELIMP(".", "test_eps_stattext")
x = _IGVA(1, lambda: [_LSH(1,4)])
# (Line 4) EUDOnStart(function () { x += x; });
@EUDFunc
def _lambda1():
    x.__iadd__(x)

EUDOnStart(_lambda1)
# (Line 5) function test_compatibility() {
@EUDFunc
def f_test_compatibility():
    # (Line 6) static var ret = 0;
    ret = EUDVariable(0)
    # (Line 7) const empty = Db(i2b4(0));
    empty = Db(i2b4(0))
    # (Line 8) const cond = Forward();
    cond = Forward()
    # (Line 10) py_exec("from helper import *\n\
    # (Line 26) ");
    exec("from helper import *\nwith expect_eperror():\n    Trigger(cond, ret.AddNumber(1 << 0))\nwith expect_eperror():\n    Trigger(empty, ret.AddNumber(1 << 1))\nwith expect_eperror():\n    Trigger(empty + 1, ret.AddNumber(1 << 2))\nwith expect_eperror():\n    SetVariables(ret, -1, EUDVariable(EncodeModifier(SetTo)))\nwith expect_eperror():\n    SetVariables(EUDVariable(), 1)\nwith expect_eperror():\n    SetVariables(f_dwread_epd(0), 1)\npv = PVariable()\nwith expect_eperror():\n    SetVariables(pv[0], 1)\n")
    # (Line 28) cond.__lshift__(Memory(empty, AtLeast, 1));
    cond.__lshift__(Memory(empty, AtLeast, 1))
    # (Line 29) if (cond) { ret += 1 << 3; }
    if EUDIf()(cond):
        ret.__iadd__(_LSH(1,3))
        # (Line 30) ret += x;
    EUDEndIf()
    ret.__iadd__(x)
    # (Line 31) if(Is64BitWireframe()) {}
    if EUDIf()(Is64BitWireframe()):
        # (Line 32) var z = EUDVariable();
        pass
    EUDEndIf()
    z = _LVAR([EUDVariable()])
    # (Line 33) return ret;
    EUDReturn(ret)
    # (Line 34) }
