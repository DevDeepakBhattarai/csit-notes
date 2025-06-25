// This program is Merge sort of one dimensional Array
#include<stdio.h>
#include<conio.h>
#define MAX_SIZE 50

void Display_Array_Element( int A[MAX_SIZE], int len)
  {
	int i;
	for(i=0; i<len; i++)
	 printf(" \t %d ", A[i]);
  }
void Merge(int A[MAX_SIZE], int left, int Mid, int right )
  {
	  int i=0,k,p, Temp[MAX_SIZE];
	  k=left; p=Mid+1;
	  
	  while(left<=Mid && p<=right)
	   {
		 if(A[left]< A[p])
			 Temp[i++]=A[left++];
		 else
			Temp[i++]=A[p++];
	    }

	while(left<=Mid)
	    Temp[i++]=A[left++];

	 while(p<=right)
	    Temp[i++]=A[p++];

	 for(i=k; i<=right; i++)
	    A[i]=Temp[i-k];
  }


 void Merge_Sort(int A[MAX_SIZE], int left, int right)
  {  // left is the lower index and right is the upper index of Array.
     // In our example right is 6.
  int Mid;
	if(left<right)
	{
		Mid=(left+right)/2;
		Merge_Sort(A, left, Mid);
		Merge_Sort(A, Mid+1, right);
		Merge(A, left, Mid,right);
	}
  }// End of function


 void main()
{
	int Len=7;// total number of array element
	int A[]={21,32,4,54,43,23,10};
	

	printf("\n Before Sorting:");
	Display_Array_Element(A,Len);

	Merge_Sort(A,0,Len-1);

	printf("\n After Sorting: ");
	Display_Array_Element(A,Len);
	getch();
}

