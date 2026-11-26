#define main original_main
#include "search.cpp"
#undef main
using B=bitset<256>;using A=array<int,6>;
struct Pole{G g;vector<array<int,3>>nb;vector<int>core;array<int,6>w;Pole(G const&h,int v):g(h.n+3){int n=h.n;U m=h.a[v];for(int i=0;i<3;i++){w[i]=lo(m);m&=m-1;w[i+3]=n+i;}for(auto[a,b]:h.edges())if(a!=v&&b!=v)g.add(a,b);for(int i=0;i<3;i++)g.add(w[i],w[i+3]);nb.resize(n);for(int i=0;i<n;i++)if(i!=v){core.push_back(i);U m=g.a[i];for(int&x:nb[i]){x=lo(m);m&=m-1;}}}};
struct S3{Pole const&p;array<int,32>c;int k;S3(Pole const&p,int k):p(p),k(k){}bool local(int v){if(v>=(int)p.nb.size())return true;U m=0;int unset=0;for(int u:p.nb[v]){if(c[u]<0)unset++;else{if(c[u]==c[v])return false;m|=1u<<c[u];}}return pc(m)<=2&&pc(m)+unset>=2;}bool dfs(int left,int used){if(!left)return true;int v=-1,best=-1;for(int i:p.core)if(c[i]<0){int s=0;for(int j:p.nb[i]){s+=4*(c[j]>=0);if(j<(int)p.nb.size())for(int h:p.nb[j])s+=c[h]>=0;}if(s>best)best=s,v=i;}for(int x=0;x<min(k,used+1);x++){c[v]=x;bool ok=local(v);for(int u:p.nb[v])ok&=local(u);if(ok&&dfs(left-1,max(used,x+1)))return true;c[v]=-1;}return false;}bool solve(A const&a){int used=*max_element(a.begin(),a.end())+1;if(used>k)return false;c.fill(-1);for(int i=0;i<6;i++)c[p.w[i]]=a[i];for(int i:p.core)if(!local(i))return false;return dfs(p.core.size()-3,used);}};
struct T3{Pole const&p;T3(Pole const&p):p(p){}bool valid(UF const&f,vector<pair<int,int>>const&neq){for(auto[a,b]:neq)if(f.r(a)==f.r(b))return false;return true;}bool dfs(UF f,vector<pair<int,int>>neq,U rem){if(!rem)return true;int v=-1;U opt=0;for(U m=rem;m;m&=m-1){int i=lo(m);U o=0;for(int j=0;j<3;j++){int a=p.nb[i][(j+1)%3],b=p.nb[i][(j+2)%3],c=p.nb[i][j];UF h=f;h.join(a,b);if(h.r(a)!=h.r(c)&&valid(h,neq))o|=1u<<j;}if(!o)return false;if(v<0||pc(o)<pc(opt)){v=i;opt=o;if(pc(o)==1)break;}}for(U m=opt;m;m&=m-1){int j=lo(m),a=p.nb[v][(j+1)%3],b=p.nb[v][(j+2)%3],c=p.nb[v][j];UF h=f;h.join(a,b);auto nn=neq;nn.emplace_back(a,c);if(dfs(h,nn,rem^(1u<<v)))return true;}return false;}bool solve(A const&a){UF f;vector<pair<int,int>>neq=p.g.edges();for(int i=0;i<6;i++)for(int j=i+1;j<6;j++){if(a[i]==a[j])f.join(p.w[i],p.w[j]);else neq.emplace_back(p.w[i],p.w[j]);}U rem=0;for(int i:p.core)rem|=1u<<i;return valid(f,neq)&&dfs(f,neq,rem);}};
A norm(A a){map<int,int>m;for(int&x:a){if(!m.count(x)){int j=m.size();m[x]=j;}x=m[x];}return a;}
int main(int argc,char**argv){int maxn=argc>1?atoi(argv[1]):14;vector<A>ps;A a{};function<void(int,int)>gen=[&](int i,int used){if(i==6){if(a[0]!=a[3]&&a[1]!=a[4]&&a[2]!=a[5])ps.push_back(a);return;}for(int j=0;j<=used;j++){a[i]=j;gen(i+1,max(used,j+1));}};gen(0,0);cerr<<"patterns "<<ps.size()<<endl;map<A,int>idx;for(int i=0;i<(int)ps.size();i++)idx[ps[i]]=i;vector<int>flip;vector<vector<int>>perms;array<int,3>perm{0,1,2};do{vector<int>v;for(auto a:ps)v.push_back(idx.at(norm({a[perm[0]],a[perm[1]],a[perm[2]],a[perm[0]+3],a[perm[1]+3],a[perm[2]+3]})));perms.push_back(v);}while(next_permutation(perm.begin(),perm.end()));for(auto a:ps)flip.push_back(idx.at(norm({a[3],a[4],a[5],a[0],a[1],a[2]})));struct Entry{B f,t;string s;int v,perm;};vector<Entry>types;set<pair<string,string>>seen;int count=0,gap=0;for(int n=4;n<=maxn;n+=2){ifstream file("graphs_"+to_string(n)+".g6");string s;if(n==4){file.close();}vector<string>input;if(n==4)input.push_back("C~");else while(file>>s)input.push_back(s);for(auto s:input){G g=parse(s);for(int v=0;v<n;v++){Pole p(g,v);S3 x(p,4);T3 y(p);B f,t;for(int i=0;i<(int)ps.size();i++){if(x.solve(ps[i]))f.set(i),t.set(i);else if(y.solve(ps[i]))t.set(i);}count++;gap+=(f!=t);for(int pp=0;pp<6;pp++){B ff,tt,rf,rt;for(int i=0;i<(int)ps.size();i++){ff[i]=f[perms[pp][i]];tt[i]=t[perms[pp][i]];rf[flip[i]]=ff[i];rt[flip[i]]=tt[i];}if(!seen.emplace(ff.to_string(),tt.to_string()).second)continue;Entry e{ff,tt,s,v,pp};for(auto h:types)if((h.f&rf).none()&&(h.t&rt).any()){cout<<"HIT "<<s<<" "<<v<<" "<<pp<<" and "<<h.s<<" "<<h.v<<" "<<h.perm<<endl;for(int i=0;i<(int)ps.size();i++)if(tt[i]&&h.t[flip[i]]){for(int c:ps[i])cout<<c;cout<<endl;}return 0;}types.push_back(e);}}}cerr<<n<<" checked "<<count<<" types "<<types.size()<<" gaps "<<gap<<endl;}
// Test two 3-poles joined on two ports, with the third joined through the 10-vertex gap fragment.
vector<B> map4(ps.size()),mapAny(ps.size());
for(int i=0;i<(int)ps.size();i++){
 auto a=ps[i];int used=*max_element(a.begin(),a.end())+1;
 for(int q=0;q<=used;q++)for(int y=0;y<=max(used,q+1);y++){
  if(q==y)continue;
  A b=norm({q,a[4],a[5],y,a[1],a[2]});auto it=idx.find(b);if(it==idx.end())continue;
  // Gap fragment state (x,y,p,q): its internal ports are the external colors of A and B.
  set<int> bd{a[0],q,a[3],y};
  mapAny[i].set(it->second);
  if(max({used,q+1,y+1})<=4 && bd.size()!=4)map4[i].set(it->second);
 }
}
int best=999;string hit;
for(auto a:types){B f,t;for(int i=0;i<(int)ps.size();i++){if(a.f[i])f|=map4[i];if(a.t[i])t|=mapAny[i];}
 for(auto b:types)if((f&b.f).none()&&(t&b.t).any()){
  int n=a.s[0]+b.s[0]-126-2+10;
  if(n<best){best=n;hit=a.s+" "+to_string(a.v)+" "+to_string(a.perm)+" / "+b.s+" "+to_string(b.v)+" "+to_string(b.perm);}
 }}
if(best<999)cout<<"GAP COMPOSITION HIT "<<best<<" "<<hit<<endl;else cout<<"NO GAP COMPOSITION HIT"<<endl;
cout<<"NO DIRECT HIT"<<endl;}
