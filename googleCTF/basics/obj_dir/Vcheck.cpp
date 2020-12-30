// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vcheck.h for the primary calling header

#include "Vcheck.h"
#include "Vcheck__Syms.h"

//==========

void Vcheck::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vcheck::eval\n"); );
    Vcheck__Syms* __restrict vlSymsp = this->__VlSymsp;  // Setup global symbol table
    Vcheck* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
#ifdef VL_DEBUG
    // Debug assertions
    _eval_debug_assertions();
#endif  // VL_DEBUG
    // Initialize
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) _eval_initial_loop(vlSymsp);
    // Evaluate till stable
    int __VclockLoop = 0;
    QData __Vchange = 1;
    do {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Clock loop\n"););
        _eval(vlSymsp);
        if (VL_UNLIKELY(++__VclockLoop > 100)) {
            // About to fail, so enable debug to see what's not settling.
            // Note you must run make with OPT=-DVL_DEBUG for debug prints.
            int __Vsaved_debug = Verilated::debug();
            Verilated::debug(1);
            __Vchange = _change_request(vlSymsp);
            Verilated::debug(__Vsaved_debug);
            VL_FATAL_MT("check.sv", 1, "",
                "Verilated model didn't converge\n"
                "- See DIDNOTCONVERGE in the Verilator manual");
        } else {
            __Vchange = _change_request(vlSymsp);
        }
    } while (VL_UNLIKELY(__Vchange));
}

void Vcheck::_eval_initial_loop(Vcheck__Syms* __restrict vlSymsp) {
    vlSymsp->__Vm_didInit = true;
    _eval_initial(vlSymsp);
    // Evaluate till stable
    int __VclockLoop = 0;
    QData __Vchange = 1;
    do {
        _eval_settle(vlSymsp);
        _eval(vlSymsp);
        if (VL_UNLIKELY(++__VclockLoop > 100)) {
            // About to fail, so enable debug to see what's not settling.
            // Note you must run make with OPT=-DVL_DEBUG for debug prints.
            int __Vsaved_debug = Verilated::debug();
            Verilated::debug(1);
            __Vchange = _change_request(vlSymsp);
            Verilated::debug(__Vsaved_debug);
            VL_FATAL_MT("check.sv", 1, "",
                "Verilated model didn't DC converge\n"
                "- See DIDNOTCONVERGE in the Verilator manual");
        } else {
            __Vchange = _change_request(vlSymsp);
        }
    } while (VL_UNLIKELY(__Vchange));
}

VL_INLINE_OPT void Vcheck::_sequent__TOP__1(Vcheck__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vcheck::_sequent__TOP__1\n"); );
    Vcheck* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Variables
    CData/*2:0*/ __Vdlyvdim0__check__DOT__memory__v0;
    CData/*6:0*/ __Vdlyvval__check__DOT__memory__v0;
    // Body
    __Vdlyvval__check__DOT__memory__v0 = vlTOPp->data;
    __Vdlyvdim0__check__DOT__memory__v0 = vlTOPp->check__DOT__idx;
    vlTOPp->check__DOT__idx = (7U & ((IData)(5U) + (IData)(vlTOPp->check__DOT__idx)));
    vlTOPp->check__DOT__memory[__Vdlyvdim0__check__DOT__memory__v0] 
        = __Vdlyvval__check__DOT__memory__v0;
    vlTOPp->check__DOT__magic = ((((QData)((IData)(
                                                   (((vlTOPp->check__DOT__memory
                                                      [0U] 
                                                      << 0x15U) 
                                                     | (vlTOPp->check__DOT__memory
                                                        [5U] 
                                                        << 0xeU)) 
                                                    | ((vlTOPp->check__DOT__memory
                                                        [6U] 
                                                        << 7U) 
                                                       | vlTOPp->check__DOT__memory
                                                       [2U])))) 
                                   << 0x1cU) | ((QData)((IData)(
                                                                ((vlTOPp->check__DOT__memory
                                                                  [4U] 
                                                                  << 7U) 
                                                                 | vlTOPp->check__DOT__memory
                                                                 [3U]))) 
                                                << 0xeU)) 
                                 | (QData)((IData)(
                                                   ((vlTOPp->check__DOT__memory
                                                     [7U] 
                                                     << 7U) 
                                                    | vlTOPp->check__DOT__memory
                                                    [1U]))));
    vlTOPp->open_safe = (0xaafef4be2dbccULL == (((QData)((IData)(
                                                                 (0x3ffU 
                                                                  & (IData)(vlTOPp->check__DOT__magic)))) 
                                                 << 0x2eU) 
                                                | (((QData)((IData)(
                                                                    (vlTOPp->check__DOT__magic 
                                                                     >> 0xaU))) 
                                                    << 0xeU) 
                                                   | (QData)((IData)(
                                                                     (0x3fffU 
                                                                      & (IData)(
                                                                                (vlTOPp->check__DOT__magic 
                                                                                >> 0x2aU))))))));
}

void Vcheck::_eval(Vcheck__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vcheck::_eval\n"); );
    Vcheck* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    if (((IData)(vlTOPp->clk) & (~ (IData)(vlTOPp->__Vclklast__TOP__clk)))) {
        vlTOPp->_sequent__TOP__1(vlSymsp);
    }
    // Final
    vlTOPp->__Vclklast__TOP__clk = vlTOPp->clk;
}

VL_INLINE_OPT QData Vcheck::_change_request(Vcheck__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vcheck::_change_request\n"); );
    Vcheck* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    return (vlTOPp->_change_request_1(vlSymsp));
}

VL_INLINE_OPT QData Vcheck::_change_request_1(Vcheck__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vcheck::_change_request_1\n"); );
    Vcheck* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    // Change detection
    QData __req = false;  // Logically a bool
    return __req;
}

#ifdef VL_DEBUG
void Vcheck::_eval_debug_assertions() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vcheck::_eval_debug_assertions\n"); );
    // Body
    if (VL_UNLIKELY((clk & 0xfeU))) {
        Verilated::overWidthError("clk");}
    if (VL_UNLIKELY((data & 0x80U))) {
        Verilated::overWidthError("data");}
}
#endif  // VL_DEBUG
