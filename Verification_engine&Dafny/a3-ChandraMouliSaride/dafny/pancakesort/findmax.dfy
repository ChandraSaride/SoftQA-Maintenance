// returns an index of the largest element of array 'a' in the range [0..n)
method findMax (a : array<int>, n : int) returns (r:int)
    requires n >= 1 && n<=a.Length;
    ensures 0<=r<n;
    ensures forall l :: 0 <= l < n ==> a[r] >= a[l];
    ensures exists l :: 0 <= l < n && a[r] == a[l];
{
  var mi;
  var i;
  mi := 0;
  i := 0;
  while (i < n)
  invariant 0 <= i <=n;
  invariant 0 <= mi <n;
  invariant forall l :: 0 <= l < i ==>  a[mi] >= a[l];
  decreases n-i;
  {
    if (a[i] > a[mi])
    { mi := i; }
    i := i + 1;
  }
  return mi;
}
