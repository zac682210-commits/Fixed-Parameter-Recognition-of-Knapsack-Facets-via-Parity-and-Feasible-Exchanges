from fractions import Fraction as F
from math import lcm

def rref(A):
 A=[[F(x) for x in row] for row in A];piv=[];r=0
 if not A:return A,piv
 for c in range(len(A[0])):
  p=next((i for i in range(r,len(A)) if A[i][c]),None)
  if p is None:continue
  A[r],A[p]=A[p],A[r];q=A[r][c];A[r]=[x/q for x in A[r]]
  for i in range(len(A)):
   if i!=r and A[i][c]:
    q=A[i][c];A[i]=[x-q*y for x,y in zip(A[i],A[r])]
  piv.append(c);r+=1
  if r==len(A):break
 return A,piv

def nullspace(A):
 R,piv=rref(A);n=len(A[0]);out=[]
 for c in range(n):
  if c in piv:continue
  w=[F(0)]*n;w[c]=F(1)
  for i,p in enumerate(piv):w[p]=-R[i][c]
  d=lcm(*[x.denominator for x in w]);out.append([int(x*d) for x in w])
 return out

def determinant(A):
 A=[[F(x) for x in row] for row in A];d=F(1)
 for c in range(len(A)):
  p=next((i for i in range(c,len(A)) if A[i][c]),None)
  if p is None:return F(0)
  if p!=c:A[p],A[c]=A[c],A[p];d=-d
  q=A[c][c];d*=q
  for i in range(c+1,len(A)):
   if A[i][c]:
    t=A[i][c]/q;A[i]=[x-t*y for x,y in zip(A[i],A[c])]
 return d

def rank(A):return len(rref(A)[1])
