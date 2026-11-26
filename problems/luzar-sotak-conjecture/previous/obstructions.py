import glob,networkx as nx
from itertools import combinations

def feasible(g, constrained=None):
    if constrained is None: constrained=list(g)
    vs=list(g); index={v:i for i,v in enumerate(vs)}; n=len(vs)
    N={index[v]:tuple(index[u] for u in g[v]) for v in constrained}
    assert all(len(x)==3 for x in N.values())
    E=tuple((index[u],index[v]) for u,v in g.edges())
    def merge(p,a,b):
        a,b=p[a],p[b]
        return p if a==b else tuple(a if x==b else x for x in p)
    def dfs(p,neq,rem):
        if not rem:return p
        best=None
        for v in rem:
            opts=[]
            for a,b,c in (N[v],(N[v][1],N[v][2],N[v][0]),(N[v][2],N[v][0],N[v][1])):
                q=merge(p,a,b)
                if q[a]!=q[c] and all(q[x]!=q[y] for x,y in neq):opts.append((q,(a,c)))
            if not opts:return None
            if best is None or len(opts)<len(best[1]):best=v,opts
            if len(opts)==1:break
        v,opts=best
        for q,pair in opts:
            w=dfs(q,neq+(pair,),rem-{v})
            if w is not None:return w
        return None
    return dfs(tuple(range(n)),E,set(N))

def edge_open(g,u,v):
    h=g.copy();h.remove_edge(u,v);h.add_edge(u,'x');h.add_edge(v,'y');return h,list(g)
def vertex_open(g,v):
    h=g.copy();nb=list(h[v]);h.remove_node(v)
    for i,u in enumerate(nb):h.add_edge(u,'x'+str(i))
    return h,[u for u in g if u!=v]

def main():
    tested=0;bridgeless=0;hits=[]
    for f in sorted(glob.glob('exceptions_*.txt')):
        for l in open(f):
            label,s,*_=l.split();assert label=='impossible';g=nx.from_graph6_bytes(s.encode());assert feasible(g) is None;tested+=1
            if list(nx.bridges(g)):continue
            bridgeless+=1
            for u,v in g.edges():
                h,core=edge_open(g,u,v)
                if feasible(h,core) is None:
                    print('ROBUST EDGE',s,(u,v),list(g.edges()),flush=True);hits.append((s,'edge',u,v))
            for v in g:
                h,core=vertex_open(g,v)
                if feasible(h,core) is None:
                    print('ROBUST VERTEX',s,v,list(g.edges()),flush=True);hits.append((s,'vertex',v))
    print('checked',tested,'bridgeless',bridgeless,'hits',len(hits))
if __name__=='__main__':main()
