#!/usr/bin/env python

import z3
from z3 import BitVec, BitVecVal, And, Or, Xor, If, Solver, Not, ZeroExt
import time
from ipdb import set_trace


PARAM = "PARAM"
CONST = "CONST"


LONG0 = "LONG0"
LONG1 = "LONG1"

long_spec = [
    [PARAM, PARAM, PARAM, PARAM],
    [PARAM, PARAM, PARAM, PARAM],
    [PARAM, PARAM, PARAM, PARAM],
    [PARAM, PARAM, PARAM, PARAM],
]

def long_func(params, type_):

    assert type_ in [LONG0, LONG1]

    def Abs(x):
        return If(x >= 0, x, -x)

    def F(x1, x2, y1, y2):
        assert x1 == x2 and y1 == y2
        return Abs(ZeroExt(24, p[x1]) * ZeroExt(24, p[x2]) - ZeroExt(24, p[y1]) * ZeroExt(24, p[y2]))

    s = Solver()
    p = [BitVec(f"p{i}", 8) for i in range(4)]

    idxs, consts = next(params)
    i1 = F(next(idxs), next(idxs), next(idxs), next(idxs))

    idxs, consts = next(params)
    i2 = F(next(idxs), next(idxs), next(idxs), next(idxs))

    if type_ == LONG0:
        s.add(i2 > i1)
    else:
        s.add(i2 <= i1)

    idxs, consts = next(params)
    i1 = F(next(idxs), next(idxs), next(idxs), next(idxs))

    idxs, consts = next(params)
    i2 = F(next(idxs), next(idxs), next(idxs), next(idxs))

    if type_ == LONG0:
        s.add(i2 <= i1)
    else:
        s.add(i1 < i2)

    s.check()
    m = s.model()
    return bytes([m.eval(pp).as_long() for pp in p])


xor_spec = [
    [PARAM, PARAM, CONST],
    [PARAM, CONST],
    [PARAM, PARAM, PARAM],
    [PARAM, PARAM, PARAM, PARAM],
]

def xor_func(params, *args):
    conds = []
    s = Solver()
    p = [BitVec(f"p{i}", 8) for i in range(4)]

    idxs, consts = next(params) # chk(2, 1)
    conds.append( p[next(idxs)] ^ p[next(idxs)] == next(consts) )

    idxs, consts = next(params) # chk(1, 1)
    conds.append( p[next(idxs)] == next(consts) )

    idxs, consts = next(params) # chk(3, 0)
    conds.append( p[next(idxs)] == ( ( ( p[next(idxs)] ^ p[next(idxs)] ) & 0x7f ) << 1 ) )

    idxs, consts = next(params) # chk(4, 0)
    conds.append( p[next(idxs)] == ( p[next(idxs)] ^ p[next(idxs)] ^ p[next(idxs)] ) )

    s.add(And(*conds))
    s.check()
    m = s.model()
    return bytes([m.eval(pp).as_long() for pp in p])


and_spec = [
    [PARAM, PARAM],
    [PARAM, PARAM],
    [PARAM, CONST],
    [PARAM, CONST],
]

def and_func(params, *args):
    conds = []
    s = Solver()
    p = [BitVec(f"p{i}", 8) for i in range(4)]

    for _ in range(2):
        idxs, consts = next(params)
        conds.append( p[next(idxs)] == p[next(idxs)] )

    for _ in range(2):
        idxs, consts = next(params)
        conds.append( p[next(idxs)] == next(consts) )

    s.add(And(*conds))
    s.check()
    m = s.model()
    return bytes([m.eval(pp).as_long() for pp in p])



add_spec = [
    [PARAM, PARAM, PARAM, CONST],
    [PARAM, PARAM, PARAM, CONST],
    [PARAM, PARAM, PARAM, CONST],
    [PARAM, PARAM, PARAM, CONST],
]

def add_func(params, *args):
    conds = []
    s = Solver()
    p = [BitVec(f"p{i}", 8) for i in range(4)]

    for _ in range(4):
        idxs, consts = next(params)
        s.add( p[next(idxs)] + p[next(idxs)] + p[next(idxs)] == next(consts) )

    assert s.check()
    m = s.model()
    return bytes([m.eval(pp).as_long() for pp in p])


or_spec = [
    [PARAM, PARAM, CONST],
    [PARAM, PARAM, CONST],
    [PARAM, PARAM, CONST],
]

def or_func(params, *args):
    conds = []
    s = Solver()
    p = [BitVec(f"p{i}", 8) for i in range(4)]

    for _ in range(3):
        idxs, consts = next(params)
        conds.append( p[next(idxs)] + p[next(idxs)] == next(consts) )

    s.add(Not(Or(*conds)))
    s.check()
    m = s.model()
    return bytes([m.eval(pp).as_long() for pp in p])


mul_spec = [
    [PARAM, CONST],
    [PARAM, CONST],
    [PARAM, PARAM, PARAM],
    [PARAM, PARAM, PARAM, PARAM, PARAM, PARAM, PARAM],
]

def mul_func(params, *args):

    def np():
        return p[next(idxs)]

    conds = []
    s = Solver()
    p = [BitVec(f"p{i}", 8) for i in range(4)]
    
    for _ in range(2):
        idxs, consts = next(params)
        s.add( np() == next(consts))

    idxs, consts = next(params)
    s.add( np() == np()*np() )

    idxs, consts = next(params)
    s.add( np() == ( np()*np() + np()*np() - np()*np()) )

    s.check()
    m = s.model()
    return bytes([m.eval(pp).as_long() for pp in p])
