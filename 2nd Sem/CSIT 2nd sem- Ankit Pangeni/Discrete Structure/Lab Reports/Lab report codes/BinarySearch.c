// Implementation of Binary Search using Recursion 
#include <stdio.h>
#include <math.h> 
#define Max 50

// Recursive Function for Binary Search
int binarySearch(int arr[], int low, int high, int key) 
{ 
    int mid;
    if (high >= low) 
	{ 
         mid = floor ((low + high) / 2 ); 
  
        // If the element is present at the middle  
        if (arr[mid] == key) 
               return mid; 
  
        // If element is smaller than mid, then it can only be present in left subarray 
       else if (arr[mid] > key) 
            return binarySearch(arr, low, mid - 1, key); 
  
        // Else the element can only be present in right subarray 
        else if (arr[mid] < key) 
       		 return binarySearch(arr, mid + 1, high, key); 
            		 
    } 
  
      // We reach here when element is not present in array  
   return -1; 
    
} 

int main()
{
   int i,low,high,key,index;
   // Must be Sorted Array
   int A[]={21,32,45,54,63,73,80,91,94,100};
   low=0;    high=9;   
   
   printf("Array:");
   for(i=0;i<high;i++)
   	printf(" \t %d",A[i]);
   	
   printf("\nEnter the Key to be searched:  ");
   scanf("%d", &key);
   
   
   index=binarySearch(A,low,high,key);
   if(index==-1)
   		printf("\n Data don't present in the given Array");
   	else
   	 	printf(" \n Data present at %d index.", index);
   return 0;  
}
