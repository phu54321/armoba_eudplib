## NOTE: THIS FILE IS GENERATED BY EPSCRIPT! DO NOT MODITY
from eudplib import *
from eudplib.epscript.helper import _RELIMP, _IGVA, _CGFW, _ARR, _VARR, _SRET, _SV, _ATTW, _ARRW, _ATTC, _ARRC, _L2V, _LVAR, _LSH
# (Line 1) import .test_eps_misc.f_switch_test;
# (Line 2) import .test_eps_misc.f_test_array;
f_switch_test = _RELIMP(".test_eps_misc", "f_switch_test")
# (Line 4) import py_warnings;
f_test_array = _RELIMP(".test_eps_misc", "f_test_array")
import warnings
# (Line 5) import .test_eps_misc as misc;
# (Line 6) function square();
misc = _RELIMP(".", "test_eps_misc")
# (Line 8) const a = [
# (Line 9) square(1),
# (Line 10) square(2),
# (Line 11) square(3),
# (Line 12) square(4),
# (Line 13) square(5)
# (Line 14) ];
a = _CGFW(lambda: [_ARR(FlattenList([f_square(1), f_square(2), f_square(3), f_square(4), f_square(5)]))], 1)[0]
# (Line 16) function testLineno() {
@EUDFunc
def f_testLineno():
    # (Line 17) const foo = py_eval("warnings.warn");
    foo = eval("warnings.warn")
    # (Line 18) foo("ㅇㅅㅇ");
    foo("ㅇㅅㅇ")
    # (Line 19) }
    # (Line 21) function square(x) {

@EUDFunc
def f_square(x):
    # (Line 22) testLineno();
    f_testLineno()
    # (Line 23) const z = EUDArray(5);
    z = EUDArray(5)
    # (Line 24) return x * x; // + z.k;
    EUDReturn(x * x)
    # (Line 25) }
    # (Line 26) const receives = py_eval('[PVariable() for _ in range(8)]');

receives = _CGFW(lambda: [eval('[PVariable() for _ in range(8)]')], 1)[0]
# (Line 27) const attack_gwpID = 4;
attack_gwpID = _CGFW(lambda: [4], 1)[0]
# (Line 28) function constv_thing() {
@EUDFunc
def f_constv_thing():
    # (Line 29) foreach(i, pvar: py_enumerate(receives)) {}
    for i, pvar in enumerate(receives):
        # (Line 30) SetMemoryXEPD(EPD(0x656FB8) + attack_gwpID/4, Add, 100 << (attack_gwpID%4 * 8), 0xFF << (attack_gwpID%4 * 8));  // cooldown +100
        pass

    # (Line 31) return a[0] + a[1] + a[2] + a[3] + a[4];
    DoActions(SetMemoryXEPD(EPD(0x656FB8) + attack_gwpID // 4, Add, _LSH(100,(attack_gwpID % 4 * 8)), _LSH(0xFF,(attack_gwpID % 4 * 8))))
    EUDReturn(a[0] + a[1] + a[2] + a[3] + a[4])
    # (Line 32) }
