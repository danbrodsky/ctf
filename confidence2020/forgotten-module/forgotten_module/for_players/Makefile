initramfs=pwn

cpio:
	cd ./${initramfs}/; find . | cpio -o -H newc -F ../${initramfs}.cpio
iso:
	mkisofs -o ./secrets.iso ./secrets/
# run:
# 	./run
# run:
# 	./sbin/kexec --initrd=example.cpio.gz -f --reuse-cmdline bzImage


