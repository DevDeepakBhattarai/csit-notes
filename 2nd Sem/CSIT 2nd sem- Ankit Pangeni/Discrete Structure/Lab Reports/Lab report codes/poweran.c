// Recursive function to implementation power(a,b)
#include <stdio.h>

int Power(int a, int n) 
{
   if(n==0)
   		return 1;
   else
   		return(a* Power(a,n-1));
}

int main() 
{
   int n,a, result;
// take input of a and n
   a = 2;
   n = 5;
   
   result=Power(a,n);
   printf("Power(%d,%d) = %d \n", a, n, result);

   return 0;
}
