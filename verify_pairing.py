import random,json,time
from pathlib import Path
r=random.Random(341329);t0=time.monotonic();checks=0;strict_one=0
for trial in range(500):
 q=r.randrange(2,7);gam=r.sample(range(1,8),q);z=[r.randrange(0,4) for _ in range(q)];w=z[:];z[0]+=2*gam[1];w[1]+=2*gam[0];ns=[max(u,v)+r.randrange(0,4) for u,v in zip(z,w)];aa=[sorted(r.randrange(1,1000) for _ in range(m)) for m in ns];d=sum(g*t for g,t in zip(gam,z));assert d==sum(g*t for g,t in zip(gam,w));cost=lambda x:sum(a*v for arr,row in zip(aa,x) for a,v in zip(arr,row));p=lambda u:[[int(i<t) for i in range(m)] for t,m in zip(u,ns)];pz=p(z);pw=p(w);b=max(cost(pz),cost(pw))
 for j in range(q):
  lo=min(z[j],w[j]);hi=max(z[j],w[j])
  for cut in range(lo+2,hi-1):
   xp=[];xq=[]
   for k,(u,v,m) in enumerate(zip(z,w,ns)):
    l=min(u,v);h=max(u,v);opts=list(range(l,h));half=len(opts)//2
    if k==j:
     left=list(range(l,cut));right=list(range(cut,h));one={left[0],right[0]};two={left[1],right[1]};rem=[i for i in opts if i not in one|two];r.shuffle(rem);one.update(rem[:half-2]);two.update(rem[half-2:]);assert len(one)==len(two)==half
    else:r.shuffle(opts);one=set(opts[:half]);two=set(opts[half:])
    xp.append([int(i<l or i in one) for i in range(m)]);xq.append([int(i<l or i in two) for i in range(m)])
   assert all(x+y==u+v for X,Y,U,V in zip(xp,xq,pz,pw) for x,y,u,v in zip(X,Y,U,V))
   assert sum(g*sum(row) for g,row in zip(gam,xp))==d==sum(g*sum(row) for g,row in zip(gam,xq))
   for X in [xp,xq]:assert 0 in X[j][lo:cut] and 1 in X[j][cut:hi]
   assert min(cost(xp),cost(xq))<=b;strict_one+=int(max(cost(xp),cost(xq))>b);checks+=1
out={'status':'PASS','seed':341329,'endpoint_pairs':500,'cut_repartitions':checks,'only_one_feasible':strict_one,'elapsed_seconds':time.monotonic()-t0};Path('pairing_results.json').write_text(json.dumps(out,indent=2));print(out)
