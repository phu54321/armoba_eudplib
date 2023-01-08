## NOTE: THIS FILE IS GENERATED BY EPSCRIPT! DO NOT MODITY
from eudplib import *
from eudplib.epscript.helper import _RELIMP, _IGVA, _CGFW, _ARR, _VARR, _SRET, _SV, _ATTW, _ARRW, _ATTC, _ARRC, _L2V, _LVAR, _LSH
# (Line 1) function test_cunit() {
@EUDFunc
def f_test_cunit():
    # (Line 2) const sp = [0x2468ACE0, 0x13579BDF, 0xFEDCBA98, 0x76543210];
    sp = _ARR(FlattenList([0x2468ACE0, 0x13579BDF, 0xFEDCBA98, 0x76543210]))
    # (Line 3) const a = [
    # (Line 4) 0, -1, -2, sp, -4 , -5, -6, -7, -8, -9,
    # (Line 5) -10, -11, -12, -13, -14, -15, -16, -17, -18,
    # (Line 6) 0x12345607, 0x89ABCDEF];
    a = _ARR(FlattenList([0, -1, -2, sp, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, 0x12345607, 0x89ABCDEF]))
    # (Line 7) const u = EPDCUnitMap(EUDVariable(EPD(a)));
    u = EPDCUnitMap(EUDVariable(EPD(a)))
    # (Line 8) var ret = 0;
    ret = _LVAR([0])
    # (Line 9) if (u.order == 0x56) ret += 1;
    if EUDIf()(_ATTC(u, 'order') == 0x56):
        ret.__iadd__(1)
        # (Line 10) if (u.owner == P8) ret += 2;
    EUDEndIf()
    if EUDIf()(_ATTC(u, 'owner') == P8):
        ret.__iadd__(2)
        # (Line 11) if (u.orderState == 0x34) ret += 4;
    EUDEndIf()
    if EUDIf()(_ATTC(u, 'orderState') == 0x34):
        ret.__iadd__(4)
        # (Line 12) if (u.orderSignal == 0x12) ret += 8;
    EUDEndIf()
    if EUDIf()(_ATTC(u, 'orderSignal') == 0x12):
        ret.__iadd__(8)
        # (Line 13) if (u.orderUnitType == 0xCDEF) ret += 16;
    EUDEndIf()
    if EUDIf()(_ATTC(u, 'orderUnitType') == 0xCDEF):
        ret.__iadd__(16)
        # (Line 14) wwrite_epd(EPD(a) + 0x50/4, 0, $U("Artanis"));
    EUDEndIf()
    f_wwrite_epd(EPD(a) + 0x50 // 4, 0, EncodeUnit("Artanis"))
    # (Line 15) if (u.orderUnitType == py_str("Artanis")) ret += 32;
    if EUDIf()(_ATTC(u, 'orderUnitType') == str("Artanis")):
        ret.__iadd__(32)
        # (Line 16) u.die();
    EUDEndIf()
    u.die()
    # (Line 17) if (a[0x4C/4] == 0x12340007) ret += 64;
    if EUDIf()(_ARRC(a, 0x4C // 4) == 0x12340007):
        ret.__iadd__(64)
        # (Line 18) if (u.is_dying()) ret += 128;
    EUDEndIf()
    if EUDIf()(u.is_dying()):
        ret.__iadd__(128)
        # (Line 19) return ret;
    EUDEndIf()
    EUDReturn(ret)
    # (Line 20) }
