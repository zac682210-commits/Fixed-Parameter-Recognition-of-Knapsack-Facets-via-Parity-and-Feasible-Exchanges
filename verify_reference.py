import itertools,random,json,time
from pathlib import Path
from exact_linear import rank
from exact_reference import solve
rng=random.Random(341328);start=time.monotonic();stats={'cases':0,'facets':0,'invalid':0,'empty':0,'zero_coefficient_cases':0,'nonempty_cells':0,'forcedcuts':0};records=[]
fixed=[([5,8,3,3,3,3],13,[2,2,1,1,1,1],4),([1,1,1],2,[0,0,0],0),([2,3,4],5,[1,1,0],1),([2,3,4],5,[1,1,0],2)]
for n in range(2,11):
 for it in range(70):
  c=[rng.randrange(0,5) for _ in range(n)];res=[rng.randrange(1,20) for _ in range(n)]
  if it%2 and any(c):
   budget=rng.randrange(1,sum(res)+1);M=budget+1;d=rng.randrange(1,sum(c)+1);a=[M*ci+r for ci,r in zip(c,res)];b=M*d+budget
   if max(a)>b:continue
  else:
   a=res;b=rng.randrange(max(a),sum(a)+1);X=list(itertools.product((0,1),repeat=n));best=max(sum(ci*xi for ci,xi in zip(c,x)) for x in X if sum(ai*xi for ai,xi in zip(a,x))<=b);d=best+rng.choice([-1,0,0,0,1])
  fixed.append((a,b,c,d))
for a,b,c,d in fixed:
 ans=solve(a,b,c,d);X=list(itertools.product((0,1),repeat=len(a)));V=[x for x in X if sum(ai*xi for ai,xi in zip(a,x))<=b];valid=all(sum(ci*xi for ci,xi in zip(c,x))<=d for x in V);assert ans['valid']==valid
 if not valid:stats['invalid']+=1
 else:
  T=[x for x in V if sum(ci*xi for ci,xi in zip(c,x))==d];dim=rank([[1]+list(x) for x in T])-1;assert ans['dimension']==dim,(a,b,c,d,ans,dim)
  if not T:stats['empty']+=1
  else:
   stats['facets']+=int(ans['facet']);stats['nonempty_cells']+=ans['cells'];stats['forcedcuts']+=ans['forcedcuts']
 stats['zero_coefficient_cases']+=int(0 in c);stats['cases']+=1
 if len(records)<4:records.append({'input':[a,b,c,d],'output':ans})
out={'status':'PASS','seed':341328,**stats,'fixed_records':records,'elapsed_seconds':time.monotonic()-start,'oracle':'Exact enumeration of bounded count profiles, NOT a runtime-certified FPT implementation.'};Path('exact_reference_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
