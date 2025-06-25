// C program to demonstrate working of extended  Euclidean Algorithm 
#include <stdio.h> 

int gcdExtended(int a, int b, int* x, int* y) 
{ 
	// Base Case 
	if (a == 0) { 
		*x = 0; 
		*y = 1; 
		return b; 
	} 

	int x1, y1; // To store results of recursive call 
	int gcd = gcdExtended(b % a, a, &x1, &y1); 

	// Update x and y using results of recursive  call 
	*x = y1 - (b / a) * x1; 
	*y = x1; 

	return gcd; 
} 


int main() 
{ 
	int a,b,x=1, y=1; 
	
	printf("\nEnter the Value of a and b to find gcd():   ");
    scanf("%d  %d", &a,&b);
	
	
	int g = gcdExtended(a, b, &x, &y); 
	
	printf("\n\n    GCD(%d, %d) = %d", a, b, g); 
	
	printf("\n\n  The Extended Euclidean Algorithm is :   "); 
	printf("  %d = %d * %d + %d * %d ", g,x,a,y,b); 
	
	return 0;
} 

