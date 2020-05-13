include "part.dfy"


method qsort(a:array<int>, l:nat, u:nat)
  requires a != null;
  requires l <= u < a.Length;
  modifies a;

  ensures sorted_between(a, l, u+1);
  decreases u-l;

{
  // complete the code for quicksort and verify the implementation
     if(u - l > 1)
 	{
 		var pi := partition(a, l, u);
 		qsort(a, l, pi);
 		qsort(a, pi + 1, u);
 	}
 	else
 	{
 		return;
 	}
}
