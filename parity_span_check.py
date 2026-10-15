import itertools,random,json,time,sys
from pathlib import Path
from exact_linear import rank
rng=random.Random(341326);start=time.monotonic();stats={'instances':0,'parity_classes':0,'pairs':0,'midpoint_forced_cuts':0};examples=[]
for n in range(2,11):
 X=list(itertools.product((0,1),repeat=n))
 for it in range(150):
  a=[rng.randrange(1,30) for _ in range(n)];c=[rng.randrange(1,5) for _ in range(n)];b=rng.randrange(max(a),sum(a)+1)
  V=[x for x in X if sum(ai*xi for ai,xi in zip(a,x))<=b];d=max(sum(ci*xi for ci,xi in zip(c,x)) for x in V);T=[x for x in V if sum(ci*xi for ci,xi in zip(c,x))==d]
  groups=[sorted([i for i in range(n) if c[i]==v],key=lambda i:(a[i],i)) for v in sorted(set(c))];K=len(groups);comps=[];cutsall=[]
  for I in groups:
   cuts=[0]+[r+1 for r in range(len(I)-1) if not any(x[I[r]]==0 and x[I[r+1]]==1 for x in T)]+[len(I)];cutsall.append(cuts)
   comps += [I[l:h] for l,h in zip(cuts,cuts[1:])]
  C=len(comps);Z=sorted(set(tuple(sum(x[i] for i in I) for I in groups) for x in T));by={}
  for z in Z:by.setdefault(tuple(t%2 for t in z),[]).append(z)
  for zs in by.values():
   stats['parity_classes']+=1
   varying=0
   for j,I in enumerate(groups):
    lo=min(z[j] for z in zs);hi=max(z[j] for z in zs);cuts=cutsall[j]
    affected=sum(l<hi and h>lo for l,h in zip(cuts,cuts[1:]));assert affected<=3,(a,b,c,d,zs,j,cuts)
    varying+=affected
    for r in range(lo+2,hi-1):
     assert r not in cuts,(a,b,c,d,zs,j,cuts,r)
     stats['midpoint_forced_cuts']+=1
   assert varying<=3*K
   for z,w in itertools.combinations(zs,2):
    stats['pairs']+=1
    v=tuple((zi+wi)//2 for zi,wi in zip(z,w));assert v in Z
  dim=rank([[1]+list(x) for x in T])-1
  assert dim <= n-C+len(by)*(3*K+1)-1
  if dim==n-1:assert C<=len(by)*(3*K+1)
  stats['instances']+=1
result={'status':'PASS','seed':341326,**stats,'elapsed_seconds':time.monotonic()-start}
Path('parity_span_checks.json').write_text(json.dumps(result,indent=2));print(result)
