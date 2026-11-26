import itertools,re
P=[(0,0,1,1),(0,0,1,2),(0,1,1,0),(0,1,1,2),(0,1,2,0),(0,1,2,2),(0,1,2,3)]
I={p:i for i,p in enumerate(P)}
def norm(x):
 d={};return tuple(d.setdefault(a,len(d)) for a in x)
def idx(x):return I.get(norm(x),-1)
def tab(op,k):
 result=[]
 for p,q,x,y in P:
  n=2 if op=='series' else 4
  # all internal boundary values; can use fresh colors (n+4 max)
  pairs=set()
  def rec(a,maxused):
   if len(a)<n:
    for v in range(min(k,maxused+2)):rec(a+[v],max(maxused,v))
    return
   if op=='series':
    u,v=a;i=idx((p,u,x,v));j=idx((v,q,u,y))
   else:
    u,v,w,z=a
    if len({x,u,w})!=2 or len({y,v,z})!=2:return
    i=idx((u,v,p,q));j=idx((w,z,p,q))
   if i>=0 and j>=0:pairs.add((i,j))
  rec([],max(p,q,x,y));result.append(pairs)
 return result
T={(o,k):tab(o,k) for o in ['series','parallel'] for k in [4,8]}
def mask(o,k,a,b):return sum(1<<i for i,pairs in enumerate(T[o,k]) if any(a>>j&1 and b>>l&1 for j,l in pairs))
R=[idx((p[1],p[0],p[3],p[2])) for p in P]
D=[idx((p[2],p[3],p[0],p[1])) for p in P]
def tr(a,r):return sum(1<<r[i] for i in range(7) if a>>i&1)
base={}
for l in open('pole_results16.txt'):
 if l.startswith('TYPE'):
  _,a,b,s,u,v=l.split();base[int(a),int(b)]=(ord(s[0])-63,('base',s,int(u),int(v)))
base[(3,3)]=(4,('base','C~',0,1))
seen=base.copy()
def add(key,n,rec):
 if key not in seen or n<seen[key][0]:seen[key]=(n,rec);return True
 return False
for wave in range(10):
 changed=0;old=list(seen.items())
 for (a,b),(n,r) in old:
  changed+=add((tr(a,R),tr(b,R)),n,('reverse',r))
 for (a,b),(n,r) in old:
  for (c,d),(m,s) in old:
   for o in ['series','parallel']:
    t=(mask(o,4,a,c),mask(o,8,b,d));changed+=add(t,n+m+2*(o=='parallel'),(o,r,s))
 print('wave',wave,'types',len(seen),'changed',changed,flush=True)
 hits=[]
 for (a,b),(n,r) in seen.items():
  for (c,d),(m,s) in seen.items():
   if not (a&tr(c,D)) and b&tr(d,D):hits.append((n+m,r,s,(a,b),(c,d)))
 if hits:
  print('HIT',min(hits,key=lambda x:x[0]),flush=True);break
 if not changed:break
print('types',sorted((a,b,n) for (a,b),(n,r) in seen.items()))
