#!/usr/bin/python

notice = r"""/*
 * glibc-compat.h
 *
 * Copyright 2021 Bill Zissimopoulos
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall NOT be removed
 * from this file.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */
"""

import sys, re

symtab = {}
for line in sys.stdin:
    line = line.rstrip()
    part = line.split("\t", 2)
    if 2 != len(part):
        continue
    part = part[1].split()
    if "GLIBC_PRIVATE" in part[1] or part[2].startswith("GLIBC_"):
        continue
    sym = part[2]
    ver = part[1]
    symtab.setdefault(sym, []).append(ver)

print(notice)
for sym in sorted(symtab.keys()):
    ver = symtab[sym]
    ver = sorted(ver, key = lambda v: [int(p) if p.isdigit() else p.lower() for p in re.split(r'(\d+)', v)])
    ver = ver[-1].lstrip("(").rstrip(")")
    print("__asm__(\".symver %s,%s@%s\");" % (sym, sym, ver))
