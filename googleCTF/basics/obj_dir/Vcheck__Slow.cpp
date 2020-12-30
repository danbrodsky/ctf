// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vcheck.h for the primary calling header

#include "Vcheck.h"
#include "Vcheck__Syms.h"

//==========

VL_CTOR_IMP(Vcheck) {
    Vcheck__Syms* __restrict vlSymsp = __VlSymsp = new Vcheck__Syms(this, name());
    Vcheck* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Reset internal values
    
    // Reset structure values
    _ctor_var_reset();
}

void Vcheck::__Vconfigure(Vcheck__Syms* vlSymsp, bool first) {
    if (false && first) {}  // Prevent unused
    this->__VlSymsp = vlSymsp;
    if (false && this->__VlSymsp) {}  // Prevent unused
    Verilated::timeunit(-12);
    Verilated::timeprecision(-12);
}

Vcheck::~Vcheck() {
    VL_DO_CLEAR(delete __VlSymsp, __VlSymsp = NULL);
}

void Vcheck::_initial__TOP__2(Vcheck__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vcheck::_initial__TOP__2\n"); );
    Vcheck* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->check__DOT__idx = 0U;
}

void Vcheck::_settle__TOP__3(Vcheck__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vcheck::_settle__TOP__3\n"); );
    Vcheck* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
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

void Vcheck::_eval_initial(Vcheck__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vcheck::_eval_initial\n"); );
    Vcheck* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->__Vclklast__TOP__clk = vlTOPp->clk;
    vlTOPp->_initial__TOP__2(vlSymsp);
}

void Vcheck::final() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vcheck::final\n"); );
    // Variables
    Vcheck__Syms* __restrict vlSymsp = this->__VlSymsp;
    Vcheck* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
}

void Vcheck::_eval_settle(Vcheck__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vcheck::_eval_settle\n"); );
    Vcheck* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->_settle__TOP__3(vlSymsp);
}

void Vcheck::_ctor_var_reset() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vcheck::_ctor_var_reset\n"); );
    // Body
    clk = VL_RAND_RESET_I(1);
    data = VL_RAND_RESET_I(7);
    open_safe = VL_RAND_RESET_I(1);
    { int __Vi0=0; for (; __Vi0<8; ++__Vi0) {
            check__DOT__memory[__Vi0] = VL_RAND_RESET_I(7);
    }}
    check__DOT__idx = VL_RAND_RESET_I(3);
    check__DOT__magic = VL_RAND_RESET_Q(56);
}
