import sys,re,collections
def load_stock(p):
    d={}
    for l in open(p):
        a=l.split(None,2)
        if len(a)==3: d[a[2].strip()]=(a[1],a[0])
    return d
def load_map(p):
    d={}
    for l in open(p):
        a=l.split()
        if len(a)==3: d[a[2]]=(a[1],a[0])
    return d
st=load_stock(sys.argv[1]); my=load_map(sys.argv[2])
print("stock symbols",len(st),"mine",len(my))
def func(t): return t in 'TtWw'
only_st=sorted(k for k,v in st.items() if func(v[0]) and k not in my)
only_my=sorted(k for k,v in my.items() if func(v[0]) and k not in st)
print("functions only in STOCK:",len(only_st)); print("functions only in MINE:",len(only_my))
pat=re.compile(r'(msm|sec|tima|qpnp|mdss|smd|scm|board|machine|early|reserve|memblock|pm_|rpm|clk|gpio|pinctrl|regulator|mach|samsung|montblanc|patek|hlte|flip|switch)',re.I)
for name,lst in (('ONLY IN STOCK',only_st),('ONLY IN MINE',only_my)):
    sel=[k for k in lst if pat.search(k)]
    print("\n=====",name,"(matching hardware/early patterns):",len(sel))
    print(" ".join(sel[:700]))
# early-boot ordering: __initcall tables / machine descriptors
for n in ('msm8974_init_very_early','msm8974_init','msm8974_init_early','msm8974_reserve','msm8974_map_io','msm_dt_match','msm8974_dt_match'):
    print(n,'stock',st.get(n),'mine',my.get(n))
