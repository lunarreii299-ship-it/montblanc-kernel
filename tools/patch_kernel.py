#!/usr/bin/env python3
"""Adds the Montblanc (SM-W2014) machine symbols to the Lineage msm8974 3.4 kernel tree."""
import re, sys, pathlib
k = pathlib.Path(sys.argv[1])

kc = k / 'arch/arm/mach-msm/Kconfig'
s = kc.read_text()
if 'SEC_MONTBLANC_PROJECT' not in s:
    add = '''
config SEC_MONTBLANC_PROJECT
	default n
	bool "Samsung Montblanc project (SM-W2014)"
	help
	  Support for Samsung Montblanc (SM-W2014) dual screen flip phone.

config MACH_MONTBLANC
	default n
	bool "Samsung model MONTBLANC"
	select SEC_MONTBLANC_PROJECT
	help
	  Support for Samsung MONTBLANC (SM-W2014) device.

'''
    s = s.replace('config SEC_PATEK_PROJECT', add.lstrip('\n') + 'config SEC_PATEK_PROJECT', 1)
    kc.write_text(s)
    print('Kconfig: added MONTBLANC symbols')

b = k / 'arch/arm/mach-msm/board-8974.c'
s = b.read_text()
old = '#ifdef CONFIG_SEC_PATEK_PROJECT'
new = '#if defined(CONFIG_SEC_PATEK_PROJECT) || defined(CONFIG_SEC_MONTBLANC_PROJECT)'
n = s.count(old)
s = s.replace(old, new)
b.write_text(s)
print('board-8974.c: widened keypad guard in', n, 'places')

# The tree's gcc wrapper is Python 2 only; make it a plain pass-through.
w = k / 'scripts/gcc-wrapper.py'
if w.exists():
    w.write_text('#!/bin/sh\nexec "$@"\n')
    w.chmod(0o755)
    print('gcc-wrapper.py replaced with pass-through')
