#define main random_experiment_main
#include "targeted.cpp"
#undef main
int main(){
    ofstream out("structured.tsv");out<<"family\tm\tk\tn\tgraph6\tstatus4\tnodes4\tstatus5\tnodes5\tstatus_unbounded\tnodes_unbounded\twitness\n";
    int count=0,unsat=0,unknown=0,none=0;uint64_t largest=0;
    auto test=[&](const Graph&g,string family,int m,int k){
        if(!g.admissible())return;
        PaletteSolver a(g,4,1000000);Status s=a.solve();count++;largest=max(largest,a.nodes);Status t=NOT_RUN,u=NOT_RUN;uint64_t tn=0,un=0;vector<int>w=a.witness;
        if(s!=SAT){unsat+=s==UNSAT;unknown+=s==UNKNOWN;PaletteSolver b(g,5,1000000);t=b.solve();tn=b.nodes;if(t==SAT){w=b.witness;assert(check_witness(g,w,5));}else{EqualitySolver c(g,1000000);u=c.solve();un=c.nodes;if(u==SAT){w=c.witness;assert(check_witness(g,w,g.n));}none+=u==UNSAT;}}
        if(s==SAT)assert(check_witness(g,w,4));
        out<<family<<'\t'<<m<<'\t'<<k<<'\t'<<g.n<<'\t'<<g.graph6()<<'\t'<<int(s)<<'\t'<<a.nodes<<'\t'<<int(t)<<'\t'<<tn<<'\t'<<int(u)<<'\t'<<un<<'\t';for(int z:w)out<<z<<',';out<<endl;
        if(s==UNSAT&&(t==SAT||u==SAT)){cerr<<"CANDIDATE "<<family<<" "<<m<<","<<k<<" "<<g.graph6()<<endl;exit(3);}
    };
    for(int m=5;m<=31;m++)for(int k=1;k<=(m-1)/2;k++){
        Graph g(2*m);for(int i=0;i<m;i++){g.add(i,(i+1)%m);g.add(i,m+i);g.add(m+i,m+(i+k)%m);}test(g,"generalized_petersen",m,k);
    }
    Graph base=Graph::parse("M??OPDDIA_ook?q??");auto e=base.edges();
    set<string>seen;
    for(int i=0;i<(int)e.size();i++)for(int j=i+1;j<(int)e.size();j++){
        auto[a,b]=e[i];auto[c,d]=e[j];Graph g(16);for(auto[u,v]:e)g.add(u,v);g.del(a,b);g.del(c,d);g.add(a,14);g.add(b,14);g.add(c,15);g.add(d,15);g.add(14,15);test(g,"subdivide_gp7_2",i,j);
        for(int swapend=0;swapend<2;swapend++){
            if(swapend)swap(c,d);
            if(a==c||a==d||b==c||b==d||base.has(a,c)||base.has(b,d))continue;
            Graph h=base;h.del(a,b);h.del(c,d);h.add(a,c);h.add(b,d);
            if(seen.insert(h.graph6()).second)test(h,"switch_gp7_2",i,2*j+swapend);
        }
    }
    cout<<"tested="<<count<<" unsat4="<<unsat<<" unknown4="<<unknown<<" unbounded_unsat="<<none<<" max_nodes4="<<largest<<endl;
}
