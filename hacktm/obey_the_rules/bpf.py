class BPFInsn:  # Filter block
    def __init__(self):
        self.code = None  # Actual filter code, word
        self.jt = None  # Jump true, byte
        self.jf = None  # Jump false, byte
        self.k = None  # Generic multiuse field, double-word

    def __repr__(self):
        return str((self.code, self.jt, self.jf, self.k))


def create():
    sock_filter = [BPFInsn() for _ in range(1)]
    sock_filter[0].code = 6
    sock_filter[0].jt = 0
    sock_filter[0].jf = 0
    sock_filter[0].k = 0x7FFF0000
    write_bpf(sock_filter, "bpf.bin")

    import struct

    open("bpf.bin", "wb").write(
        "".join(struct.pack("<HBBI", c.code, c.jt, c.jf, c.k) for c in sock_filter)
    )


def parse():
    rules = "2000000004000000"
    rules += "1500000a3e0000c0"
    rules += "2000000000000000"
    rules += "3500080000000040"
    rules += "1500060002000000"
    rules += "1500050038000000"
    rules += "1500000500000000"
    rules += "2000000010000000"
    rules += "1500000203000000"
    rules += "2000000018000000"
    rules += "1500000188286000"
    rules += "060000000000ff7b"
    rules += "0600000000000000"
    rules += "0000000000000000"
    rules += "0000000000000000"
    rules += "0000000000000000"
    rules += "0000000000000000"
    rules += "0000000000000000"

    sock_filter = []
    for i in range(0, len(rules), 16):
        sf = BPFInsn()
        sf.code = int(rules[i : i + 4], 16)
        sf.jt = int(rules[i + 4 : i + 6], 16)
        sf.jf = int(rules[i + 6 : i + 8], 16)
        sf.k = int(rules[i + 8 : i + 16], 16)
    open("server_bpf.bin", "wb").write(rules.decode("hex"))


parse()
