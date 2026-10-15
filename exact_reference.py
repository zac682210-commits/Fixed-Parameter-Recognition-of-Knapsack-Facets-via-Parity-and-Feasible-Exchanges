"""Exact reference implementation of parity-cell rank algorithm.
The oracle ENUMERATES bounded count vectors; it is not an implementation of
Lenstra/Kannan and has no claimed FPT running time. All ranks use Fraction.
"""
import itertools
from exact_linear import rank,nullspace

def affine_basis(points):
 if not points:return []
 first=points[0];k=len(first);chosen=[first];W=[[0]*k]
 while True:
  added=False
  for q in nullspace(W):
   point=next((z for z in points if sum(qi*(zi-ui) for qi,zi,ui in zip(q,z,first))!=0),None)
   if point is not None:
    chosen.append(point);W.append([zi-ui for zi,ui in zip(point,first)]);added=True;break
  if not added:return chosen

def solve(a,b,c,d):
 n=len(a);groups=[sorted([i for i in range(n) if c[i]==v],key=lambda i:(a[i],i)) for v in sorted(set(c))];gam=[c[I[0]] for I in groups];q=len(groups)
 arrays=[[a[i] for i in I] for I in groups];F=[[0]+list(itertools.accumulate(A)) for A in arrays]
 allz=list(itertools.product(*[range(len(I)+1) for I in groups]));cost=lambda z:sum(f[t] for f,t in zip(F,z));value=lambda z:sum(g*t for g,t in zip(gam,z));feasz=[z for z in allz if cost(z)<=b]
 if any(value(z)>d for z in feasz):return {'valid':False,'dimension':None}
 Z=[z for z in feasz if value(z)==d]
 if not Z:return {'valid':True,'dimension':-1,'facet':False}
 def prefix(z):
  x=[0]*n
  for I,t in zip(groups,z):
   for i in I[:t]:x[i]=1
  return x
 rows=[];cutsall=[]
 for j,(I,A,f) in enumerate(zip(groups,arrays,F)):
  cuts=[0]
  for r in range(len(I)-1):
   other=A[:r]+A[r+2:]
   witness=next((z for z in Z if 1<=z[j]<len(I) and cost(z)-f[z[j]]+A[r+1]+sum(other[:z[j]-1])<=b),None)
   if witness is None:cuts.append(r+1)
   else:
    v=[0]*(n+1);v[1+I[r]]=1;v[1+I[r+1]]=-1;rows.append(v)
  cuts.append(len(I));cutsall.append(cuts)
 by={}
 for z in Z:by.setdefault(tuple(t%2 for t in z),[]).append(z)
 cells=0;selected=[];forcedcuts=0
 for zs in by.values():
  bounds=[(min(z[j] for z in zs),max(z[j] for z in zs)) for j in range(q)];parts={}
  for j,(l,h) in enumerate(bounds):
   for r in range(l+2,h-1):assert r not in cutsall[j];forcedcuts+=1
  for z in zs:
   key=tuple(0 if z[j]==l else 2 if z[j]==h else 1 for j,(l,h) in enumerate(bounds));parts.setdefault(key,[]).append(z)
  for pts in parts.values():
   cells+=1
   for z in affine_basis(pts):selected.append(z);rows.append([1]+prefix(z))
 C=sum(len(t)-1 for t in cutsall);dimension=rank(rows)-1
 assert dimension<=n-C+len(by)*(3*q+1)-1
 return {'valid':True,'dimension':dimension,'facet':dimension==n-1,'q':q,'components':C,'cells':cells,'selected_profiles':len(selected),'parities':len(by),'forcedcuts':forcedcuts}
