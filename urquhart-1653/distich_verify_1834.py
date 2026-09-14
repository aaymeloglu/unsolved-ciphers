import re
t = open('mait.txt', encoding='utf-8', errors='ignore').read()
end = t.find('THE  CYPHRAL  DISTICH')
seg = t[end-60000:end]
seg = re.sub(r'(?m)^\s*(\d)\s+(\d)\s*\.', r'\1\2.', seg)
marks = [(int(m.group(1)), m.start(), m.end()) for m in re.finditer(r'(?m)^\s*(\d{1,2})\s*\.\s+', seg)]
parts = {}
for k, (n, s, e) in enumerate(marks):
    nxt = marks[k+1][1] if k+1 < len(marks) else len(seg)
    body = re.sub(r'(?m)^.*(PROQUIRITATIONS|LOGOPANDECTEISION).*$', '', seg[e:nxt])
    body = re.sub(r'-\s*\n\s*', '', body)
    parts.setdefault(n, body)
W = {n: re.findall(r"[A-Za-z][A-Za-z'’]*", parts[n]) for n in range(1, 33)}
print("wordcounts", [len(W[n]) for n in range(1,33)])
L1 = [5,3,27,38,32,14,21,8,66,8,70,39,5,9,12,18,2,3,56,5,1,7,3,2,13,19,3,25,9,3,16,6]
L2 = [25,15,13,6,11,20,5,1,2,12,1,20,20,49,20,20,35,33,4,6,8,35,5,38,5,5,18,10,3,11,32,42]
T1 = "OGODUPHOLDKINGCHARLSTHESECONDAND"; T2 = "MAKEHIMTHESUPREMERULEROFTHISLAND"
for L, T in ((L1, T1), (L2, T2)):
    out = ''.join(W[i][n-1][0].upper() if n-1 < len(W[i]) else '?' for i, n in enumerate(L, 1))
    print(out, sum(a == b for a, b in zip(out, T)), '/32')
    print('  words:', [W[i][n-1] for i, n in enumerate(L, 1)])
# show first 12 words of each section as a sanity check of segmentation
for n in (1,11,15,17,32):
    print(n, ' '.join(W[n][:12]))
