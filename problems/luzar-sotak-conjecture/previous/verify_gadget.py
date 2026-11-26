"""Independent exhaustive verification of the ten-vertex boundary gadget."""
from itertools import product
# Internals: p,q,u,v,a,b,s,t,r,w. x,y are external stubs.
edges = [('p','u'),('p','v'),('q','u'),('q','v'),('u','a'),('v','b'),('a','b'),('a','s'),('b','t'),('s','r'),('s','w'),('t','r'),('t','w'),('r','w'),('x','p'),('y','q')]
internal = 'pquvabstrw'
vertices = internal+'xy'
N = {v:[] for v in vertices}
for a,b in edges:
    N[a].append(b);N[b].append(a)
assert all(len(N[v]) == 3 for v in internal)
def valid(c):
    return all(c[a]!=c[b] for a,b in edges) and all(len({c[u] for u in N[v]})==2 for v in internal)
fixed = {'p':0,'q':1,'x':2,'y':3}
free = [v for v in vertices if v not in fixed]
assert len(free)==8
count4=0
for vals in product(range(4),repeat=8):
    if valid(fixed | dict(zip(free,vals))):count4+=1
assert count4==0
witness = fixed | {'u':4,'v':4,'a':0,'b':1,'s':4,'t':4,'r':0,'w':1}
assert valid(witness)
assert set(witness.values())==set(range(5))
print('All 65,536 assignments to eight unfixed vertices with four colors: 0 valid.')
print('Five-color witness:',witness)
