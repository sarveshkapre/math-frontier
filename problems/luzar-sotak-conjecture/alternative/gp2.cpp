#define main random_experiment_main
#include "targeted.cpp"
#undef main
int main(){
    cout<<"m,status3,nodes3,status4,nodes4,outer,inner\n";
    for(int m=5;m<=31;m++){
        Graph g(2*m);for(int i=0;i<m;i++){g.add(i,(i+1)%m);g.add(i,m+i);g.add(m+i,m+(i+2)%m);}
        PaletteSolver a(g,3,1000000),b(g,4,1000000);Status s=a.solve();Status t=NOT_RUN;vector<int>w=a.witness;
        if(s!=SAT){t=b.solve();w=b.witness;}
        if(!w.empty())assert(check_witness(g,w,t==NOT_RUN?3:4));
        cout<<m<<','<<int(s)<<','<<a.nodes<<','<<int(t)<<','<<b.nodes<<',';
        for(int i=0;i<m&&(int)w.size()==g.n;i++)cout<<w[i];cout<<',';
        for(int i=m;i<g.n&&(int)w.size()==g.n;i++)cout<<w[i];cout<<'\n';
    }
}
