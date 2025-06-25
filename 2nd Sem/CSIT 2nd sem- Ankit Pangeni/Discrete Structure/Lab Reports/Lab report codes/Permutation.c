// Implementation of permutation using recursion
#include <stdio.h>

int factorial(int n) {
   int f;
   for(f = 1; n > 1; n--)
       f *= n;
   return f;
}

int nPr(int n,int r) {
   return factorial(n)/factorial(n-r);
}

int main() 
{
   int n, r;
// take input of n and r
   printf("\nEnter the Value of n and r for Permutation:   ");
   scanf("%d  %d", &n,&r);

   printf("%dP%d = %d \n", n, r, nPr(n,r));

   return 0;
}
