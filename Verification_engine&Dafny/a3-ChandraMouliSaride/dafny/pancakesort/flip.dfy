// flips (i.e., reverses) array elements in the range [0..num]
method flip (a: array<int>, num: int)
requires num >= 0 && num<= a.Length-1;
modifies a;
ensures forall i:: 0 <= i <=num==> a[i] == old(a[num-i]) && a[num-i]==old(a[i]);
ensures forall i:: num<i<=a.Length-1 ==> a[i] == old(a[i])
{ 
  var tmp:int;

  var i := 0;
  var j := num;
  while (i < j)
  invariant 0<=i<=num;
  invariant 0<=j<=num;
  invariant i+j==num;
  invariant forall z :: i<=z<=j==>a[z]==old(a[z]);
  invariant forall z :: 0 <= z < i || j < z <= num ==> a[num-z] == old(a[z]) && a[z] == old(a[num-z]);
  invariant forall z:: num<z<=a.Length-1 ==> a[z] == old(a[z])
  decreases j;
  {
    tmp := a[i];
    a[i] := a[j];
    a[j] := tmp;
    i := i + 1;
    j := j - 1;
  }
}
