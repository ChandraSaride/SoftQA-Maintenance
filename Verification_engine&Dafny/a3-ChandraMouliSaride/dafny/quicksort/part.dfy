include "preds.dfy"

method choose(l:nat, u:nat) returns (rv: nat)
  requires l <= u;
  ensures l <= rv <= u;
{rv := l;}

method partition(a:array<int>, l:nat, u:nat) returns (pivot:int)
  modifies a;
  requires a != null;
  requires l <= u < a.Length;
  requires l>0 ==> partitioned(a, 0, l-1, l, u);
  requires u+1 <= a.Length -1 ==> partitioned(a, l, u, u+1, a.Length-1);

  ensures l <= pivot <= u;

  ensures l > 0 ==> beq(old(a[..]), a[..], 0, l-1);
  ensures l > 0 ==> partitioned(a, 0, l-1, l, u);

  ensures u < a.Length-1 ==> beq(old(a[..]), a[..], u+1, a.Length - 1);
  ensures u < a.Length - 1 ==> partitioned(a, l, u, u+1, a.Length-1);

  ensures pivot > l ==> partitioned(a, l, pivot-1, pivot, pivot);
  ensures pivot < u ==> partitioned(a, pivot, pivot, pivot+1, u);
{
  var pi := choose(l, u);
  var pv := a[pi];

  a[pi] := a[u];
  a[u] := pv;

  var i:int := l - 1;
  var j := l;
  while (j < u)
    // MISSING INVARIANT
  invariant l<=j<=u;
  invariant pv==a[u];
  invariant l-1<=i<j;
  invariant l > 0 ==> beq(old(a[..]), a[..], 0, l-1);
  invariant l > 0 ==> partitioned(a, 0, l-1, l, u);
  invariant u < a.Length-1 ==> beq(old(a[..]), a[..], u+1, a.Length - 1);
  invariant u < a.Length - 1 ==> partitioned(a, l, u, u+1, a.Length-1);
  invariant forall z :: l<=z<=i ==> a[z]<=pv;
  invariant forall z :: i<z<j ==> a[z]>=pv;
  {
    if (a[j] <= pv)
    {
      i := i + 1;
      var t := a[i];
      a[i] := a[j];
      a[j] := t;
    }
    j := j + 1;
  }

  pivot := i + 1;
  var t := a[pivot];
  a[pivot] := a[u];
  a[u] := t;
}