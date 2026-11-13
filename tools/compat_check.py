import re,sys,subprocess
dts=open(sys.argv[1],errors='replace').read()
comp=set()
for m in re.finditer(r'compatible\s*=\s*([^;]+);',dts):
    for s in re.findall(r'"([^"]+)"',m.group(1)): comp.add(s)
vm=open(sys.argv[2],'rb').read()
stockk=open(sys.argv[3],'rb').read() if len(sys.argv)>3 else b''
miss=sorted(c for c in comp if c.encode() not in vm)
print("DT compatible strings:",len(comp)," not found in MY kernel:",len(miss))
if stockk:
    ms=[c for c in miss if c.encode() in stockk]
    print("of those, matched by STOCK kernel (=> my kernel lacks/renamed the driver):",len(ms))
    print("\n".join(ms))
    print("not matched by either:",[c for c in miss if c not in ms])
else:
    print("\n".join(miss))
