## NOTE: THIS FILE IS GENERATED BY EPSCRIPT! DO NOT MODITY
from eudplib import *
from eudplib.epscript.helper import _RELIMP, _IGVA, _CGFW, _ARR, _VARR, _SRET, _SV, _ATTW, _ARRW, _ATTC, _ARRC, _L2V, _LVAR, _LSH
# (Line 1) function test_cunit() {
@EUDFunc
def f_test_cunit():
    # (Line 2) const a = [0x12345607, 0x89ABCDEF];
    a = _ARR(FlattenList([0x12345607, 0x89ABCDEF]))
    # (Line 3) const u = EPDCUnitMap(EUDVariable(EPD(a) - 19));
    u = EPDCUnitMap(EUDVariable(EPD(a) - 19))
    # (Line 4) var ret = 0;
    ret = _LVAR([0])
    # (Line 5) if (u.order == 0x56) ret += 1;
    if EUDIf()(_ATTC(u, 'order') == 0x56):
        ret.__iadd__(1)
        # (Line 6) if (u.owner == P8) ret += 2;
    EUDEndIf()
    if EUDIf()(_ATTC(u, 'owner') == P8):
        ret.__iadd__(2)
        # (Line 7) if (u.orderState == 0x34) ret += 4;
    EUDEndIf()
    if EUDIf()(_ATTC(u, 'orderState') == 0x34):
        ret.__iadd__(4)
        # (Line 8) if (u.orderSignal == 0x12) ret += 8;
    EUDEndIf()
    if EUDIf()(_ATTC(u, 'orderSignal') == 0x12):
        ret.__iadd__(8)
        # (Line 9) if (u.orderUnitType == 0xCDEF) ret += 16;
    EUDEndIf()
    if EUDIf()(_ATTC(u, 'orderUnitType') == 0xCDEF):
        ret.__iadd__(16)
        # (Line 10) wwrite_epd(EPD(a) + 1, 0, $U("Artanis"));
    EUDEndIf()
    f_wwrite_epd(EPD(a) + 1, 0, EncodeUnit("Artanis"))
    # (Line 11) if (u.orderUnitType == py_str("Artanis")) ret += 32;
    if EUDIf()(_ATTC(u, 'orderUnitType') == str("Artanis")):
        ret.__iadd__(32)
        # (Line 12) return ret;
    EUDEndIf()
    EUDReturn(ret)
    # (Line 13) }
