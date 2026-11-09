#!/usr/bin/env python3
"""Replace only the kernel inside an Android boot/recovery image. usage: swap_kernel.py in.img zImage out.img"""
import struct, sys, hashlib
src, kern, out = sys.argv[1:4]
d = open(src, 'rb').read()
assert d[:8] == b'ANDROID!'
ksz, kaddr, rsz, raddr, ssz, saddr, tags, page, dtsz, osv = struct.unpack('<10I', d[8:48])
n = lambda x: (x + page - 1) // page * page
o = page
old_k = d[o:o+ksz]; o += n(ksz)
r = d[o:o+rsz]; o += n(rsz)
s = d[o:o+ssz]; o += n(ssz)
dt = d[o:o+dtsz]
K = open(kern, 'rb').read()
hdr = bytearray(d[:page])
if len(sys.argv) > 4:
    hdr[64:576] = sys.argv[4].encode().ljust(512, b'\0')
struct.pack_into('<I', hdr, 8, len(K))
h = hashlib.sha1()
for b in (K, r, s, dt):
    h.update(b); h.update(struct.pack('<I', len(b)))
hdr[576:608] = h.digest().ljust(32, b'\0')
pad = lambda b: b + b'\0' * (-len(b) % page)
img = bytes(hdr) + pad(K) + pad(r) + pad(s) + pad(dt)
open(out, 'wb').write(img)
print('old kernel', ksz, 'new kernel', len(K), 'ramdisk', rsz, 'dt', dtsz, 'cmdline', d[64:576].split(b'\0')[0].decode())
print('image', len(img))
