import itertools,random,json,time,sys
from pathlib import Path
from exact_linear import rank
rng=random.Random(341327);start=time.monotonic();stats={'instances':0,'parity_classes':0,'nontrivial_parities':0,'forced_cuts':0,'affine_pieces':0};records=[]
for K in range(1,6):
 for it in range(120):
  ns=[rng.randrange(4,11) for _ in range(K)];gam=rng.sample(range(1,10),K);d=rng.randrange(1,sum(s*g for s,g in zip(ns,gam))+1);aa=[sorted(rng.randrange(1,30) for _ in range(n)) for n in ns];F=[[0]+list(itertools.accumulate(a)) for a in aa]
  ZZ=[z for z in itertools.product(*[range(n+1) for n in ns]) if sum(g*t for g,t in zip(gam,z))==d]
  if not ZZ:continue
  costs={z:sum(f[t] for f,t in zip(F,z)) for z in ZZ};b=rng.randrange(min(costs.values()),max(costs.values())+1);Z=[z for z in ZZ if costs[z]<=b];cutsall=[]
  for j,(a,n,f) in enumerate(zip(aa,ns,F)):
   cuts=[0]
   for r in range(n-1):
    other=[a[t] for t in range(n) if t not in (r,r+1)]
    if not any(1<=z[j]<n and costs[z]-f[z[j]]+a[r+1]+sum(other[:z[j]-1])<=b for z in Z):cuts.append(r+1)
   cuts+=[n];cutsall.append(cuts)
  def u(z):return [min(max(z[j]-l,0),h-l) for j,cuts in enumerate(cutsall) for l,h in zip(cuts,cuts[1:])]
  C=sum(len(cuts)-1 for cuts in cutsall);by={}
  for z in Z:by.setdefault(tuple(t%2 for t in z),[]).append(z)
  for zs in by.values():
   stats['parity_classes']+=1;stats['nontrivial_parities']+=int(len(zs)>1)
   bounds=[]
   for j in range(K):
    lo=min(z[j] for z in zs);hi=max(z[j] for z in zs);bounds.append((lo,hi));cuts=cutsall[j]
    affected=sum(l<hi and h>lo for l,h in zip(cuts,cuts[1:]));assert affected<=3,(K,aa,d,b,zs,j,cuts)
    for r in range(lo+2,hi-1):assert r not in cuts;stats['forced_cuts']+=1
   pieces={}
   for z in zs:
    tag=tuple(0 if z[j]==lo else 2 if z[j]==hi else 1 for j,(lo,hi) in enumerate(bounds));pieces.setdefault(tag,[]).append(z)
   for vs in pieces.values():
    stats['affine_pieces']+=1
    A=[[1]+list(z) for z in vs];Q=[u(z) for z in vs]
    assert rank([a+q for a,q in zip(A,Q)])==rank(A),(aa,b,gam,d,vs,cutsall)
  r=rank([[1]+u(z) for z in Z]);assert r<=len(by)*(3*K+1)
  if r==C:assert C<=(3*K+1)*2**K
  stats['instances']+=1
result={'status':'PASS','seed':341327,**stats,'elapsed_seconds':time.monotonic()-start};Path('profile_parity_checks.json').write_text(json.dumps(result,indent=2));print(result)
