#!/usr/bin/env python3
"""Minimal Samsung/QCDT boot.img (v0) packer. usage: mkbootimg.py kernel ramdisk dt out [cmdline]"""
import struct, sys, hashlib
kernel, ramdisk, dt, out = sys.argv[1:5]
cmd = sys.argv[5] if len(sys.argv) > 5 else 'console=null androidboot.hardware=qcom user_debug=31 msm_rtb.filter=0x3F'
page = 2048
base = 0
K, R, D = (open(p, 'rb').read() for p in (kernel, ramdisk, dt))
hdr = b'ANDROID!' + struct.pack('<10I', len(K), base + 0x8000, len(R), base + 0x02000000, 0, base + 0x00f00000,
                                base + 0x01e00000, page, len(D), 0)
hdr += b'\0' * 16 + cmd.encode().ljust(512, b'\0')
h = hashlib.sha1()
for b in (K, R, b'', D):
    h.update(b); h.update(struct.pack('<I', len(b)))
hdr += h.digest().ljust(32, b'\0') + b'\0' * 1024
pad = lambda b: b + b'\0' * (-len(b) % page)
img = pad(hdr) + pad(K) + pad(R) + pad(D)
open(out, 'wb').write(img)
print('boot image', len(img), 'bytes')
