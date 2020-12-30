from pwn import *
from capstone import *
import re
from ipdb import set_trace
from z3lib import *
from IPython import embed


# TODO this prob needs to be adjusted
ALL_FUNCS_LEN = 4556 + 260
DEBUG = True


def iterify(params):
    return ((iter(x), iter(y)) for x,y in params)

def fmt(block):
    s = ""
    for inst in block:
        name, ops = inst[2:4]
        s += f"{name:<10} {ops}\n"
    return s.strip("\n")

def mypp(block):
    if isinstance(block[0], list):
        for b in block:
            print(fmt(b) + "\n")
    else:
        print(fmt(block))

def addiu_idx(inst):
    #   (68, 4, 'addiu', '$v0, $v0, 2'),
    name = inst[2]
    ops  = inst[3]
    assert name == "addiu"
    m = re.search(r"\$v[01], \$v[01], ([123])", ops)
    assert m
    return int(m.group(1))

def get_const(inst):
    # (76, 4, 'addiu', '$v0, $zero, 0x95'),
    ops = inst[3]
    name = inst[2]
    assert name == "addiu"
    m = re.search(r"\$zero, (0x)?(.+)", ops)
    assert m
    if m.group(1):
        base = 16
    else:
        base = 10
    return int(m.group(2), base)

def log(s):
    if DEBUG:
        print(s)

def next_addiu_or_zero(block_iter):
    found_lw = False
    count_since_lw = 0
    for inst in block_iter:
        name = inst[2]
        ops  = inst[3]
        log(f"{name:<10} {ops}")
        if found_lw is False and name == "lw":
            found_lw = True
            count_since_lw += 1
            continue
        if found_lw:
            if name == "lbu":
                log(f"Found lbu so idx is zero {name}")
                return 0
            elif name == "addiu" and re.search("\$v[01], \$v[01],", ops):
                log(f"Found addiu so idx {name}")
                return addiu_idx(inst)
    assert 0

def next_const(block_iter):
    # block is generator
    for inst in block_iter:
        name = inst[2]
        if name == "bnez" or name == "beqz":
            # Weird, hit a branch when expecting to see another register load
            # Assume compiler skipped it b/c null
            return 0
        name = inst[2]
        ops  = inst[3]
        if name == "addiu" and "$zero" in ops:
            return get_const(inst)
    assert 0

def parse_spec(blocks, spec):
    params_list = []
    for block, ss in zip(blocks, spec):
        log(f"Parsing spec {ss} for block:\n{fmt(block)}\n=====================")
        params = []
        idxs = []
        consts = []
        block_iter = iter(block)
        for s in ss:
            log(f"Looking for {s}")
            if s == PARAM:
                idxs.append(next_addiu_or_zero(block_iter))
            elif s == CONST:
                consts.append(next_const(block_iter))
            else:
                assert 0
        params += [idxs, consts]
        params_list.append(params)
    return params_list


class Func:

    xor = [250, 280]
    and_ = [176, 184]
    mul = [308, 328]
    or_ = [190, 210]
    long = [440, 444]
    add = [300, 304]

    tag = None
    count = None
    long_type = None

    def __init__(self, insts):
        self.blocks = []
        self.jmp_block = None
        self.ret_block = None
        self.count = 0
        self.parse(insts)
        self.id_func()
        # Should NEVER touch insts again b/c it's generator

    def __repr__(self):
        s = "<Func >"
        if self.tag:
            s += self.tag
        return s
    
    def id_func(self):

        def in_range(c, r):
            return r[0] <= c <= r[1]

        # multiply by 4 b/c each instruction is 4 bytes long
        count = self.count * 4
        if in_range(count, self.long):
            tag = "long"
            parse_func = self.parse_long
            solve_func = long_func
        elif in_range(count, self.add):
            tag = "add"
            parse_func = self.parse_add
            solve_func = add_func
        elif in_range(count, self.mul):
            tag = "mul"
            parse_func = self.parse_mul
            solve_func = mul_func
        elif in_range(count, self.or_):
            tag = "or"
            parse_func = self.parse_or
            solve_func = or_func
        elif in_range(count, self.and_):
            tag = "and"
            parse_func = self.parse_and
            solve_func = and_func
        elif in_range(count, self.xor):
            tag = "xor"
            parse_func = self.parse_xor
            solve_func = xor_func
        else:
            assert 0, "Messed up range search"

        self.parse_func = parse_func
        self.solve_func = solve_func
        self.tag = tag
        
    def parse(self, insts):
        assert not self.blocks and not self.jmp_block and not self.ret_block and self.count == 0
        b = []
        for inst in insts:
            self.count += 1
            b.append(inst)
            # name = inst.mnemonic
            name = inst[2]
            if name.startswith("b"):
                # Branch
                self.blocks.append(b)
                b = []
            elif name == "jal":
                self.jmp_block = b
                b = []
            elif name == "jr":
                # return is always at the end
                self.ret_block = b
                if not self.jmp_block or not self.blocks:
                    assert 0
                break
        assert self.count > 10

    def solve(self):
        params = self.parse_func()
        self.params = params
        return self.solve_func(iterify(params), self.long_type)

    def parse_xor(self):
        assert len(self.blocks) == 5
        return parse_spec(self.blocks, xor_spec)

    def parse_add(self):
        assert len(self.blocks) == 5
        return parse_spec(self.blocks, add_spec)

    def parse_mul(self):
        assert len(self.blocks) == 5
        return parse_spec(self.blocks, mul_spec)

    def parse_or(self):
        assert len(self.blocks) == 4
        return parse_spec(self.blocks, or_spec)

    def parse_and(self):
        assert len(self.blocks) == 5
        return parse_spec(self.blocks, and_spec)

    def parse_long(self):
        # Get type
        b = self.blocks[2]
        assert len(b) == 4
        name = b[3][2]
        if name == "bnez":
            self.long_type = LONG1
        elif name == "beqz":
            self.long_type = LONG0
        else:
            assert 0
        # Get rid of the tiny blocks so they don't mess up the spec parsing
        self.blocks = [b for b in self.blocks if len(b) >= 6]
        assert len(self.blocks) == 4
        return parse_spec(self.blocks, long_spec)


md = Cs(CS_ARCH_MIPS, CS_MODE_MIPS32)


def disasm(x):
    print("="*80)
    print("="*80)
    return list(md.disasm_lite(bytes.fromhex(x), 0))


def test_all():

    t0 = time.time()

    # =============================================================================================
    # XOR
    # =============================================================================================
    xor1 = disasm("e0ffbd271c00bfaf1800beaf25f0a0032000c4af2000c28f03004224000043902000c28f0000429026106200ff0043305c0002242c006214000000002000c28f00004390ed00022427006214000000002000c28f01004224000043902000c28f03004224000044902000c28f0000429026108200ff00423040100200ff00423019006214000000002000c28f02004224000043902000c28f03004224000044902000c28f0000429026108200ff0044302000c28f010042240000429026108200ff00423008006214000000002000c28f04004224252040001c07100c0000000002000010000000002510000025e8c0031c00bf8f1800be8f2000bd270800e00300000000")
    xor2 = disasm("e0ffbd271c00bfaf1800beaf25f0a0032000c4af2000c28f01004224000043902000c28f020042240000429026106200ff004330ec0002242e006214000000002000c28f02004224000043909500022428006214000000002000c28f03004224000043902000c28f01004224000044902000c28f020042240000429026108200ff00423040100200ff00423019006214000000002000c28f000043902000c28f01004224000044902000c28f020042240000429026108200ff0044302000c28f030042240000429026108200ff00423008006214000000002000c28f04004224252040008a06100c0000000002000010000000002510000025e8c0031c00bf8f1800be8f2000bd270800e00300000000")
    f1 = Func(xor1)
    f2 = Func(xor2)

    assert f1.tag == "xor"
    assert f2.tag == "xor"

    params = parse_spec(f1.blocks, xor_spec)
    assert params == [[[3, 0], [92]], [[0], [237]], [[1, 3, 0], []], [[2, 3, 0, 1], []]]
    r = xor_func(iterify(params))

    f = Func(xor1)
    r = f.solve()

    # =============================================================================================
    # AND
    # =============================================================================================

    and1 = disasm("e0ffbd271c00bfaf1800beaf25f0a0032000c4af2000c28f000043902000c28f02004224000042901c006214000000002000c28f03004224000043902000c28f010042240000429014006214000000002000c28f0300422400004390a10002240e006214000000002000c28f02004224000043906800022408006214000000002000c28f0400422425204000d806100c0000000002000010000000002510000025e8c0031c00bf8f1800be8f2000bd270800e00300000000")
    f = Func(and1)
    params = parse_spec(f.blocks, and_spec)
    r = and_func(iterify(params))

    assert f.tag == "and"

    f = Func(and1)
    r = f.solve()

    and2 = disasm("e0ffbd271c00bfaf1800beaf25f0a0032000c4af2000c28f03004224000043902000c28f01004224000042901a006214000000002000c28f02004224000043902000c28f0000429013006214000000002000c28f02004224000042900e004014000000002000c28f0100422400004390f000022408006214000000002000c28f04004224252040001a05100c0000000002000010000000002510000025e8c0031c00bf8f1800be8f2000bd270800e00300000000")
    f = Func(and2)
    r = f.solve()

    # =============================================================================================
    # OR
    # =============================================================================================

    or1 = disasm("e0ffbd271c00bfaf1800beaf25f0a0032000c4af2000c28f0300422400004290251840002000c28f0000429021186200040002241d006210000000002000c28f00004290251840002000c28f010042240000429021186200b500022413006210000000002000c28f0100422400004290251840002000c28f0200422400004290211862002700022408006210000000002000c28f0400422425204000b605100c0000000002000010000000002510000025e8c0031c00bf8f1800be8f2000bd270800e00300000000")
    f = Func(or1)
    params = parse_spec(f.blocks, or_spec)
    assert params == [[[3, 0], [4]], [[0, 1], [181]], [[1, 2], [39]]]
    r = or_func(iterify(params))

    assert f.tag == "or"

    f = Func(or1)
    r = f.solve()

    # =============================================================================================
    # ADD
    # =============================================================================================
    add1 = disasm("e0ffbd271c00bfaf1800beaf25f0a0032000c4af2000c28f0100422400004290251840002000c28f0200422400004290211062002000c38f0300632400006390211843004301022432006214000000002000c28f0200422400004290251840002000c28f0300422400004290211062002000c38f00006390211843008001022424006214000000002000c28f0300422400004290251840002000c28f00004290211062002000c38f0100632400006390211843008001022416006214000000002000c28f00004290251840002000c28f0100422400004290211062002000c38f020063240000639021184300dc00022408006214000000002000c28f04004224252040009b04100c0000000002000010000000002510000025e8c0031c00bf8f1800be8f2000bd270800e00300000000")
    f = Func(add1)
    params = parse_spec(f.blocks, add_spec)
    assert params == [[[1, 2, 3], [323]],
                      [[2, 3, 0], [384]],
                      [[3, 0, 1], [384]],
                      [[0, 1, 2], [220]]]
    r = add_func(iterify(params))

    assert f.tag == "add"

    f = Func(add1)
    r = f.solve()

    # =============================================================================================
    # MUL
    # =============================================================================================
    mul1 = disasm("e0ffbd271c00bfaf1800beaf25f0a0032000c4af2000c28f000043905e0002243e006214000000002000c28f0100422400004390c200022438006214000000002000c28f0200422400004290251840002000c28f00004290252040002000c28f000042901800820012100000ff0042302a006214000000002000c28f03004224000043902000c28f01004224000044902000c28f01004224000042901800820012100000ff0044302000c28f02004224000045902000c28f02004224000042901800a20012100000ff00423021108200ff0044302000c28f000045902000c28f000042901800a20012100000ff00423023108200ff00423008006214000000002000c28f04004224252040005706100c0000000002000010000000002510000025e8c0031c00bf8f1800be8f2000bd270800e00300000000")
    f = Func(mul1)
    params = parse_spec(f.blocks, mul_spec)
    assert params == [[[0], [94]], [[1], [194]], [[2, 0, 0], []], [[3, 1, 1, 2, 2, 0, 0], []]]
    r = mul_func(iterify(params))

    f = Func(mul1)
    r = f.solve()

    # =============================================================================================
    # LONG
    # =============================================================================================
    long1 = disasm("e0ffbd271c00bfaf1800beaf25f0a0032000c4af2000c28f0300422400004290251840002000c28f030042240000429018006200121000002000c38f0200632400006390252060002000c38f0200632400006390180083001218000023104300020041040000000023100200252040002000c28f00004290251840002000c28f0000429018006200121000002000c38f0100632400006390252860002000c38f01006324000063901800a30012180000231043000200410400000000231002002a10820036004010000000002000c28f00004290251840002000c28f0000429018006200121000002000c38f0300632400006390252060002000c38f0300632400006390180083001218000023104300020041040000000023100200252040002000c28f0100422400004290251840002000c28f010042240000429018006200121000002000c38f0200632400006390252860002000c38f02006324000063901800a30012180000231043000200410400000000231002002a10820008004014000000002000c28f04004224252040008905100c0000000002000010000000002510000025e8c0031c00bf8f1800be8f2000bd270800e00300000000")
    f = Func(long1)
    params = f.parse_long()
    assert params == [[[3, 3, 2, 2], []],
                      [[0, 0, 1, 1], []],
                      [[0, 0, 3, 3], []],
                      [[1, 1, 2, 2], []]]
    r = long_func(iterify(params), LONG0)
    # assert r == b'Q\xe1A\x81'

    assert f.tag == "long"

    f = Func(long1)
    r = f.solve()

    # =============================================================================================
    # LONG2
    # =============================================================================================
    long2 = disasm("e0ffbd271c00bfaf1800beaf25f0a0032000c4af2000c28f0300422400004290251840002000c28f030042240000429018006200121000002000c38f0200632400006390252060002000c38f0200632400006390180083001218000023104300020041040000000023100200252040002000c28f00004290251840002000c28f0000429018006200121000002000c38f0100632400006390252860002000c38f01006324000063901800a30012180000231043000200410400000000231002002a10820036004014000000002000c28f00004290251840002000c28f0000429018006200121000002000c38f0300632400006390252060002000c38f0300632400006390180083001218000023104300020041040000000023100200252040002000c28f0100422400004290251840002000c28f010042240000429018006200121000002000c38f0200632400006390252860002000c38f02006324000063901800a30012180000231043000200410400000000231002002a10820008004010000000002000c28f0400422425204000ce04100c0000000002000010000000002510000025e8c0031c00bf8f1800be8f2000bd270800e00300000000")
    f = Func(long2)
    params = f.parse_long()
    assert params == [[[3, 3, 2, 2], []],
                      [[0, 0, 1, 1], []],
                      [[0, 0, 3, 3], []],
                      [[1, 1, 2, 2], []]]
    r = long_func(iterify(params), LONG0)
    # assert r == b'\x9f?\x19f'

    assert f.tag == "long"

    f = Func(long2)
    r = f.solve()


    # =============================================================================================
    # =============================================================================================
    # BLAH
    # =============================================================================================
    # =============================================================================================

    end_func_bytes = bytes.fromhex("f8ffbd270400beaf25f0a0030800c4af01c0023cbeba423425e8c0030400be8f0800bd270800e00300000000")
    
    with open("code.1", "rb") as f:
        elf = f.read()

    m = re.search(end_func_bytes, elf)
    assert m
    # Start of the first intesting func in BYTE ORDER not exec order
    start = m.span()[1]

    assert start == 0xb5c

    insts = md.disasm_lite(elf[start:start+ALL_FUNCS_LEN], 0)
    funcs = []
    for _ in range(16):
        funcs.append(Func(insts))

    results = []
    for f in funcs:
        results.append(f.solve())

    r = list(zip(funcs, results))
        
    t1 = time.time()
    print(f"That took {t1 - t0} seconds")
    embed(colors="linux")


if __name__ == "__main__":
    test_all()
