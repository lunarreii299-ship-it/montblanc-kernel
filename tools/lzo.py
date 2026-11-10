import struct, zlib, sys, re

def lzo1x(src):
    out = bytearray(); ip = 0; state = 0
    def lits(c):
        nonlocal ip
        out.extend(src[ip:ip+c]); ip += c
    def match(mpos, cnt):
        if mpos < 0: raise ValueError('bad match offset')
        for _ in range(cnt):
            out.append(out[mpos]); mpos += 1
    def ext(base):
        nonlocal ip
        start = ip
        while src[ip] == 0: ip += 1
        v = (ip - start) * 255 + base + src[ip]; ip += 1
        return v
    if src[ip] > 17:
        t = src[ip] - 17; ip += 1
        lits(t)
        state = 4 if t >= 4 else t
    while True:
        t = src[ip]; ip += 1
        if t < 16:
            if state == 0:
                if t == 0: t = ext(15)
                lits(t + 3); state = 4; continue
            elif state != 4:
                nxt = t & 3
                mpos = len(out) - 1 - (t >> 2) - (src[ip] << 2); ip += 1
                match(mpos, 2)
            else:
                nxt = t & 3
                mpos = len(out) - 0x801 - (t >> 2) - (src[ip] << 2); ip += 1
                match(mpos, 3)
        elif t >= 64:
            nxt = t & 3
            mpos = len(out) - 1 - ((t >> 2) & 7) - (src[ip] << 3); ip += 1
            match(mpos, (t >> 5) - 1 + 2)
        elif t >= 32:
            t &= 31
            if t == 0: t = ext(31)
            v = src[ip] | (src[ip+1] << 8); ip += 2
            mpos = len(out) - 1 - (v >> 2); nxt = v & 3
            match(mpos, t + 2)
        else:
            mpos = len(out) - ((t & 8) << 11)
            t &= 7
            if t == 0: t = ext(7)
            v = src[ip] | (src[ip+1] << 8); ip += 2
            mpos -= v >> 2; nxt = v & 3
            if mpos == len(out): break
            mpos -= 0x4000
            match(mpos, t + 2)
        state = nxt
        if nxt: lits(nxt)
    return bytes(out)

def lzop_extract(buf, off):
    p = off + 9
    ver, libver, vneed = struct.unpack('>HHH', buf[p:p+6]); p += 6
    method, level = buf[p], buf[p+1]; p += 2
    flags = struct.unpack('>I', buf[p:p+4])[0]; p += 4
    if flags & 0x800: p += 4
    p += 4 + 4 + 4
    nl = buf[p]; p += 1 + nl
    p += 4
    if flags & 0x40:
        el = struct.unpack('>I', buf[p:p+4])[0]; p += 4 + el + 4
    out = bytearray()
    while True:
        usz = struct.unpack('>I', buf[p:p+4])[0]; p += 4
        if usz == 0: break
        csz = struct.unpack('>I', buf[p:p+4])[0]; p += 4
        ad = None
        if flags & 1: ad = struct.unpack('>I', buf[p:p+4])[0]; p += 4
        if flags & 0x100: p += 4
        if csz < usz:
            if flags & 2: p += 4
            if flags & 0x200: p += 4
            blk = lzo1x(buf[p:p+csz])
        else:
            blk = buf[p:p+csz]
        p += csz
        if len(blk) != usz: raise ValueError('block size mismatch %d != %d' % (len(blk), usz))
        if ad is not None and zlib.adler32(blk) & 0xffffffff != ad: raise ValueError('adler mismatch')
        out += blk
    return bytes(out)

if __name__ == '__main__':
    d = open(sys.argv[1], 'rb').read()
    i = d.find(b'\x89LZO\x00\r\n\x1a\n')
    print('lzop magic at', i)
    k = lzop_extract(d, i)
    open(sys.argv[2], 'wb').write(k)
    print('decompressed', len(k))
