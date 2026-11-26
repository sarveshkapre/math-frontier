#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <numeric>
#include <random>
#include <set>
#include <string>
#include <unordered_set>
#include <vector>
using namespace std;
using U=uint64_t;
static int pop(U x){return __builtin_popcountll(x);}
static int lo(U x){return __builtin_ctzll(x);}
struct Graph {
    int n; vector<U> adj;
    Graph(int n=0):n(n),adj(n){}
    bool has(int u,int v)const{return (adj[u]>>v)&1;}
    void add(int u,int v){assert(u!=v&&!has(u,v));adj[u]|=U(1)<<v;adj[v]|=U(1)<<u;}
    void del(int u,int v){assert(has(u,v));adj[u]^=U(1)<<v;adj[v]^=U(1)<<u;}
    vector<pair<int,int>> edges()const{vector<pair<int,int>>e;for(int u=0;u<n;u++)for(int v=u+1;v<n;v++)if(has(u,v))e.emplace_back(u,v);return e;}
    string graph6()const{assert(n<63);string s(1,char(n+63));int b=0,j=0;for(int v=1;v<n;v++)for(int u=0;u<v;u++){b=b*2+has(u,v);if(++j==6){s+=char(b+63);b=j=0;}}if(j)s+=char((b<<(6-j))+63);return s;}
    static Graph parse(string s){int n=s[0]-63;Graph g(n);int b=0;for(int v=1;v<n;v++)for(int u=0;u<v;u++,b++)if(((s[1+b/6]-63)>>(5-b%6))&1)g.add(u,v);return g;}
    bool admissible()const {
        // Connected, bridgeless, cubic, triangle-free, non-bipartite.
        for(int v=0;v<n;v++){
            if(pop(adj[v])!=3)return false;
            for(U m=adj[v];m;m&=m-1)if(adj[lo(m)]&adj[v])return false;
        }
        vector<int>disc(n,-1),low(n),color(n,-1);int timer=0;bool bridge=false,bip=true;
        function<void(int,int)>dfs=[&](int v,int par){disc[v]=low[v]=timer++;for(U m=adj[v];m;m&=m-1){int w=lo(m);if(disc[w]<0){color[w]=1-color[v];dfs(w,v);low[v]=min(low[v],low[w]);if(low[w]>disc[v])bridge=true;}else if(w!=par)low[v]=min(low[v],disc[w]);if(color[w]==color[v])bip=false;}};
        color[0]=0;dfs(0,-1);return timer==n&&!bridge&&!bip;
    }
};
enum Status{UNSAT=0,SAT=1,UNKNOWN=2,NOT_RUN=3};
struct PaletteSolver {
    const Graph &g;int k;uint64_t limit,nodes=0;vector<int>witness;
    vector<array<int,4>> scopes,tuples;vector<U> incidence;
    PaletteSolver(const Graph&g,int k,uint64_t limit):g(g),k(k),limit(limit),incidence(g.n){
        for(int v=0;v<g.n;v++){array<int,4>s{v,0,0,0};U m=g.adj[v];for(int j=1;j<4;j++){s[j]=lo(m);m&=m-1;}scopes.push_back(s);for(int u:s)incidence[u]|=U(1)<<v;}
        for(int a=0;a<k;a++)for(int b=0;b<k;b++)for(int c=0;c<k;c++)for(int d=0;d<k;d++)if(a!=b&&a!=c&&a!=d&&((b==c)+(b==d)+(c==d)==1))tuples.push_back({1<<a,1<<b,1<<c,1<<d});
    }
    bool propagate(vector<int>&domains,U todo){
        while(todo){int v=lo(todo);todo&=todo-1;auto s=scopes[v];array<int,4>support{};
            for(auto t:tuples)if((domains[s[0]]&t[0])&&(domains[s[1]]&t[1])&&(domains[s[2]]&t[2])&&(domains[s[3]]&t[3]))for(int j=0;j<4;j++)support[j]|=t[j];
            for(int j=0;j<4;j++){if(!support[j])return false;int u=s[j];if(domains[u]!=support[j]){domains[u]=support[j];todo|=incidence[u]&~(U(1)<<v);}}
        }return true;
    }
    Status dfs(vector<int>d,U todo){
        if(nodes>=limit)return UNKNOWN;
        nodes++;
        if(!propagate(d,todo))return UNSAT;
        int v=-1,bestsize=k+1,bestscore=-1;
        for(int u=0;u<g.n;u++){int size=pop(d[u]);if(size<=1)continue;int score=0;for(U m=incidence[u];m;m&=m-1)for(int w:scopes[lo(m)])score+=pop(d[w])==1;if(size<bestsize||(size==bestsize&&score>bestscore)){v=u;bestsize=size;bestscore=score;}}
        if(v<0){witness=d;for(int &c:witness)c=lo(c);return SAT;}
        for(U m=d[v];m;m&=m-1){auto copy=d;copy[v]=m&-m;Status s=dfs(move(copy),incidence[v]);if(s!=UNSAT)return s;}
        return UNSAT;
    }
    Status solve(){vector<int>d(g.n,(1<<k)-1);d[0]=1;d[lo(g.adj[0])]=2;return dfs(move(d),(U(1)<<g.n)-1);}
};
bool check_witness(const Graph&g,const vector<int>&c,int k){
    if((int)c.size()!=g.n)return false;
    for(int v=0;v<g.n;v++){if(c[v]<0||c[v]>=k)return false;set<int>s;for(U m=g.adj[v];m;m&=m-1){int w=lo(m);if(c[v]==c[w])return false;s.insert(c[w]);}if(s.size()!=2)return false;}return true;
}
struct EqualitySolver {
    const Graph&g;uint64_t limit,nodes=0;vector<array<int,3>>nb;vector<int>witness;
    EqualitySolver(const Graph&g,uint64_t limit):g(g),limit(limit){for(int v=0;v<g.n;v++){array<int,3>a;U m=g.adj[v];for(int&u:a){u=lo(m);m&=m-1;}nb.push_back(a);}}
    vector<int>merge(vector<int>p,int a,int b){int x=p[a],y=p[b];for(int&z:p)if(z==y)z=x;return p;}
    bool consistent(const vector<int>&p,const vector<pair<int,int>>&neq){for(auto[a,b]:neq)if(p[a]==p[b])return false;return true;}
    Status dfs(vector<int>p,vector<pair<int,int>>neq,U rem){if(nodes>=limit)return UNKNOWN;nodes++;if(!rem){witness=p;return SAT;}
        int v=-1;vector<int>opts;
        for(U m=rem;m;m&=m-1){int u=lo(m);vector<int>o;for(int j=0;j<3;j++){int a=nb[u][(j+1)%3],b=nb[u][(j+2)%3],c=nb[u][j];auto q=merge(p,a,b);if(q[a]!=q[c]&&consistent(q,neq))o.push_back(j);}if(o.empty())return UNSAT;if(v<0||o.size()<opts.size()){v=u;opts=o;if(o.size()==1)break;}}
        for(int j:opts){int a=nb[v][(j+1)%3],b=nb[v][(j+2)%3],c=nb[v][j];auto q=merge(p,a,b);auto nn=neq;nn.emplace_back(a,c);Status s=dfs(move(q),move(nn),rem^(U(1)<<v));if(s!=UNSAT)return s;}return UNSAT;
    }
    Status solve(){vector<int>p(g.n);iota(p.begin(),p.end(),0);return dfs(move(p),g.edges(),(U(1)<<g.n)-1);}
};
Graph fresh(int n,mt19937_64&rng){
    // Configuration model, rejection of loops and multiple edges. Unconditioned
    // simple outputs are uniform labelled cubic graphs; subsequent filters apply.
    vector<int>stubs(3*n);for(int i=0;i<3*n;i++)stubs[i]=i/3;
    for(;;){shuffle(stubs.begin(),stubs.end(),rng);Graph g(n);bool ok=true;for(int i=0;i<3*n;i+=2){int u=stubs[i],v=stubs[i+1];if(u==v||g.has(u,v)){ok=false;break;}g.add(u,v);}if(ok&&g.admissible())return g;}
}
Graph mutate(Graph g,mt19937_64&rng){
    for(int trial=0;trial<200;trial++){auto e=g.edges();int i=rng()%e.size(),j=rng()%e.size();if(i==j)continue;auto[a,b]=e[i];auto[c,d]=e[j];if(rng()%2)swap(c,d);if(a==c||a==d||b==c||b==d||g.has(a,c)||g.has(b,d))continue;Graph h=g;h.del(a,b);h.del(c,d);h.add(a,c);h.add(b,d);if(h.admissible())return h;}return g;
}
int main(int argc,char**argv){
    int per_order=argc>1?stoi(argv[1]):1000;uint64_t seed=argc>2?stoull(argv[2]):2611260711ULL;mt19937_64 rng(seed);
    ofstream samples("samples.tsv"),hard("hardest.tsv"),exceptions("exceptions.tsv");
    samples<<"n\tmode\tgraph6\tstatus4\tnodes4\twitness4\n";hard<<"n\tgraph6\tnodes4\twitness4\n";exceptions<<"n\tgraph6\tstatus4\tnodes4\tstatus5\tnodes5\tstatus_unbounded\tnodes_unbounded\n";
    cout<<"seed="<<seed<<" per_order="<<per_order<<" node_limit=1000000\n";
    cout<<"n,fresh,mutated,total,sat4,unsat4,unknown4,unbounded_impossible,counterexamples,max_nodes4,elapsed_seconds"<<endl;
    auto begin=chrono::steady_clock::now();
    for(int n:{18,22,26,30,34,40,50}){
        vector<pair<uint64_t,Graph>>pool;unordered_set<string>seen;int count=0,fresh_count=0,mut_count=0,sat=0,unsat=0,unknown=0,impossible=0,counterexamples=0;uint64_t maxnodes=0;Graph hardg;vector<int>hardw;
        while(count<per_order){bool isfresh=count<per_order/2||pool.empty();Graph g=isfresh?fresh(n,rng):mutate(pool[rng()%pool.size()].second,rng);string code=g.graph6();if(!seen.insert(code).second)continue;count++;fresh_count+=isfresh;mut_count+=!isfresh;
            PaletteSolver four(g,4,1000000);Status s=four.solve();sat+=s==SAT;unsat+=s==UNSAT;unknown+=s==UNKNOWN;
            if(s==SAT)assert(check_witness(g,four.witness,4));
            samples<<n<<'\t'<<(isfresh?"fresh":"mutated")<<'\t'<<code<<'\t'<<int(s)<<'\t'<<four.nodes<<'\t';for(int c:four.witness)samples<<c;samples<<'\n';
            if(four.nodes>maxnodes){maxnodes=four.nodes;hardg=g;hardw=four.witness;}
            if(pool.size()<32||four.nodes>pool.back().first){pool.emplace_back(four.nodes,g);sort(pool.begin(),pool.end(),[](auto&a,auto&b){return a.first>b.first;});if(pool.size()>32)pool.pop_back();}
            if(s!=SAT){PaletteSolver five(g,5,1000000);Status t=five.solve();if(t==SAT)assert(check_witness(g,five.witness,5));Status u=NOT_RUN;uint64_t unodes=0;
                if(s==UNSAT&&t==SAT){counterexamples++;ofstream ce("counterexample.g6");ce<<code<<'\n';ofstream cw("counterexample_witness.txt");for(int c:five.witness)cw<<c<<' ';cw<<'\n';}
                if(t!=SAT){EqualitySolver e(g,1000000);u=e.solve();unodes=e.nodes;if(u==SAT)assert(check_witness(g,e.witness,n));if(u==UNSAT)impossible++;if(s==UNSAT&&u==SAT){counterexamples++;ofstream ce("counterexample.g6");ce<<code<<'\n';ofstream cw("counterexample_witness.txt");for(int c:e.witness)cw<<c<<' ';cw<<'\n';}}
                exceptions<<n<<'\t'<<code<<'\t'<<int(s)<<'\t'<<four.nodes<<'\t'<<int(t)<<'\t'<<five.nodes<<'\t'<<int(u)<<'\t'<<unodes<<endl;
                if(counterexamples){cerr<<"CANDIDATE COUNTEREXAMPLE at order "<<n<<" graph6 "<<code<<endl;return 3;}
            }
        }
        hard<<n<<'\t'<<hardg.graph6()<<'\t'<<maxnodes<<'\t';for(int c:hardw)hard<<c;hard<<endl;
        double seconds=chrono::duration<double>(chrono::steady_clock::now()-begin).count();cout<<n<<','<<fresh_count<<','<<mut_count<<','<<count<<','<<sat<<','<<unsat<<','<<unknown<<','<<impossible<<','<<counterexamples<<','<<maxnodes<<','<<seconds<<endl;
    }
    return 0;
}
