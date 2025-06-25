// Implementation of Combination using recursion
#include <stdio.h>

int factorial(int n) {
   int f;
   for(f = 1; n > 1; n--)
       f *= n;
   return f;
}

int nCr(int n,int r) {
   return factorial(n)/( factorial(r)*factorial(n-r));
}

int main() 
{
   int n, r;
   
// take input of n and r
    printf("\nEnter the Value of n and r for Combination:   ");
    scanf("%d  %d", &n,&r);
   
   printf("%dC%d = %d \n", n, r, nCr(n,r));

   return 0;
}
