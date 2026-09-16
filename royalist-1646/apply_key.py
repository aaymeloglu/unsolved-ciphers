#!/usr/bin/env python3
"""Render a ciphertext file with a key file of lines 'NUM text' (text may be a letter, word, or 'null').
Usage: python3 apply_key.py key129.txt f10_ct.txt
"""
import re, sys
key={}
for ln in open(sys.argv[1]):
    ln=ln.split('#')[0].strip()
    if not ln: continue
    n,t=ln.split(None,1); key[n]=t.strip()
for ln in open(sys.argv[2]):
    if ln.startswith('#'): print(ln.rstrip()); continue
    out=[]
    for tok in re.findall(r'\[[^\]]*\]|\S+',ln):
        if tok.startswith('['): out.append(tok); continue
        v=key.get(tok.rstrip('?'))
        out.append((v if v is not None else '<'+tok+'>') if v!='null' else '')
    print(' '.join(out))
