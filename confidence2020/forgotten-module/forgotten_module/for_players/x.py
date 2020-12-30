from pwn import *
import subprocess


def bash(cmd):
    return subprocess.check_output(cmd.split(" ")).decode('UTF-8')

r = remote("forgotten-module.zajebistyc.tf", 31002)

print(r.clean(2))

r.interactive()
# enc = r.recvuntil(b"Solution:").split(b"\n")[0].decode("latin-1")

# dec = bash(enc).rstrip()

# r.sendline(dec)

# print(r.recvuntil(b"Size of initramfs in bytes: "))
# size = os.stat("./example.cpio").st_size
# print(f"File is {size} bytes")
# assert(size < 10 * 1024 * 1024)
# r.sendline(str(size))

r.sendline("6552545")
r.send(open("./pwn.cpio.gz", "rb").read())

# CHUNK_SIZE = 16384
# with open("pwn.cpio", "rb") as pwn:
#     data = pwn.read(CHUNK_SIZE)
#     while data:
#         print("Sending...")
#         r.send(data)
#         data = pwn.read(CHUNK_SIZE)

print("kexec --initrd=new.cpio -f --reuse-cmdline tinylinux2")
print("mount -t iso9660 /dev/hdc /media/cdrom")
r.interactive()

# p4{3s55y9.jpg}


# https://gist.github.com/chrisdone/02e165a0004be33734ac2334f215380e
# http://man7.org/linux/man-pages/man8/kexec.8.html
# https://wiki.osdev.org/PCI_IDE_Controller#IDE_Interface
# https://www.kernel.org/doc/html/latest/ide/ide.html
# https://www.reddit.com/r/LinuxCirclejerk/comments/32logy/the_pure_linux_kernel_is_less_than_10_mb_you_do/
# http://tldp.org/HOWTO/SCSI-2.4-HOWTO/sr.html

# cat /proc/kallsyms

# Those damn millenials and their USBs and NVMEs! They forgot to compile my IDE module. Now i can't access my secrets stored on a trusty CD-ROM. Can you help me?
