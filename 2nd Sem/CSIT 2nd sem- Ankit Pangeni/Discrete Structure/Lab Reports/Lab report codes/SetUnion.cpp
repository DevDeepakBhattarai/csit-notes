#include<stdio.h>
#include<conio.h>
#define MAX 40

void create(int set[], int);
int Union(int set1[],int, int set2[],int, int set3[]);

int main()
{
 int set1[MAX],set2[MAX],set3[MAX],L,i;
 int N,M;  // Lenth of set1 is N , Lenth of set2 is M 
 
    printf("\nNo. of elements in the SET1 : ");
       scanf("%d",&N);
       
   printf("\nNo. of elements in the SET2: ");
       scanf("%d",&M);
       
   printf("\n +++++++++++++++++++++++++++++++++++++++++++++++++++++++\n");  
   
   printf("Enter elements of SET1");
       create(set1,N);
       
   printf("Enter elements of SET2");
       create(set2,M);
       
    printf("\n *******************************************************\n");     
     
	 L=Union(set1,N,set2,M,set3);
	  
    printf("\n Union of two sets :          ");
    for(i=0;i<=L;i++)
       printf("%d  ",set3[i]);
       
  }
 
 void create(int set[],int n)
   {  
      int i,x;
      printf("\nEnter set elements : \n");
       for(i=0;i<n;i++)
       scanf("%d",&set[i]);
    }
 
  int Union(int set1[],int n, int set2[],int m,int set3[])
  {
	   int k,i,j,flag=0;
	    
		for(k=0;k<n;k++)
			 set3[k]=set1[k];
		 
		k--; 
		
		for(i=0;i<m;i++)
		{
			 flag=1;
		  for(j=0;j<n;j++)
			  {	 
			     if(set2[i]==set1[j])
			          flag=0;
		          }
		          
		  if(flag==1)
		    set3[++k]=set2[i];
	   }
	   
	 return k;
 }
 
