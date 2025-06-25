#include<stdio.h>
#include<conio.h>
#define MAX 40

void create(int set[], int);
void Crossproduct(int set1[],int, int set2[], int);

int main()
{
 int set1[MAX],set2[MAX],set3[MAX],L,i;
 int N,M;  // Lenth of set1 is N , Lenth of set2 is M 
 
   printf("\nNo. of elements in the SET1 : ");
       scanf("%d",&N);
       
   printf("\nNo. of elements in the SET2: ");
       scanf("%d",&M);
       
   printf("\n +++++++++++++++++++++++++++++++++++++++++\n");  
   
   printf("Enter elements of SET1");
       create(set1,N);
       
   printf("Enter elements of SET2");
       create(set2,M);
       
    printf("\n **************** Finding Cross Product *********************\n");     
     
	 Crossproduct(set1,N,set2,M);
	  
}
 
 void create(int set[],int n)
   {  
      int i;
      printf("\nEnter set elements : \n");
       for(i=0;i<n;i++)
       		scanf("%d",&set[i]);
    }
 
 
  void Crossproduct(int set1[],int n, int set2[],int m)
  {
	   int i,j;
	    
	 printf("\n Cross Product of two sets are:   ");
	 		
		for(i=0;i<n;i++)
		{
			
		  for(j=0;j<m;j++)
			  {	 
			    printf("   (%d, %d)",set1[i],set2[j]); 
		          
		        }
       }
 }
 

