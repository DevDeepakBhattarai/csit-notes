#include<stdio.h>
#include<conio.h>
#define MAX 40

    	 
int U[]={1,2,3,4,5,6,7,8,9,0}; // Universal Set

void create(int set[], int);
int SetComplement(int set1[],int n, int set3[]);

int main()
{
 int set1[MAX],set3[MAX],L,i;
 int N;  // Lenth of set1 is N , Lenth of set2 is M 
 
    printf("\nThe Universal Set is:   ");
    for(i=0;i<10;i++)
          printf("%d  ",U[i]);
	
	printf("\nNo. of elements in the SET1 : ");
       scanf("%d",&N);
       
   
    printf("Enter elements of SET1");
       create(set1,N);
       
    L=SetComplement(set1,N,set3);
	  
    printf("\n Set Complement of SET1:  ");
     for(i=0;i<L;i++)
          printf("%d  ",set3[i]);
    
    
}
 
 void create(int set[],int n)
   {  
      int i;
      printf("\nEnter set elements : \n");
       for(i=0;i<n;i++)
       scanf("%d",&set[i]);
    }
 
   
 int SetComplement(int set1[],int n,int set3[])
  {
	   int k=0,i,j,flag;
	    
				
	for(i=0;i<10;i++)
		{
			 flag=1;
		  for(j=0;j<n;j++)
			  {	 
			     if(U[i]==set1[j])
			        {
					  flag=0;
			          break;
			         }
		        }
		          
		  if(flag==1)
		    set3[k++]=U[i];
	   }
	   
	 return k--;
 }
