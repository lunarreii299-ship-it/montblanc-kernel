#!/usr/bin/env python3
"""Extract the raw kernel Image from the stock (LZO) zImage. usage: extract_stock_image.py zImage out.Image"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lzo
d = open(sys.argv[1], 'rb').read()
for m in re.finditer(rb'\x89LZO\x00\r\n\x1a\n', d):
    try:
        k = lzo.lzop_extract(d, m.start())
        open(sys.argv[2], 'wb').write(k)
        print('extracted', len(k), 'bytes from lzop stream at', m.start())
        sys.exit(0)
    except Exception as e:
        print('magic at', m.start(), 'is not the payload:', e)
sys.exit('no usable LZO payload found')
