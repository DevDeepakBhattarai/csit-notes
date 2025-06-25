#include<stdio.h>
#define Max 5  // Number of Vertices

//   (0)-----------(1)------(4)
//    |             |      /
//    |             |     /
//    |             |   /
//   (2)-----------(3)/



//Add edge. set arr[src][dest] = 1
void addEdge(int arr[][Max],int src, int dest)
{
     arr[src][dest] = 1;
}

//print the Adjancey Matrix
void printAdjMatrix(int arr[][Max])
{
     int i, j;
     
    printf("\n\t\t0\t1\t2\t3\t4");
    printf("\n\t--------------------------------------------");
     for(i = 0; i < Max; i++)
     {
       printf("\n\t%d|",i);
         for(j = 0; j < Max; j++)
         {
             printf("\t%d ", arr[i][j]);
         }
    printf("\n\t--------------------------------------------");
     }
}


int main()
{
    int adjMatrix[Max][Max]={0};

    addEdge(adjMatrix,0,1);
    addEdge(adjMatrix,1,0);
    addEdge(adjMatrix,0,2);
    addEdge(adjMatrix,2,0);
    addEdge(adjMatrix,2,3);
    addEdge(adjMatrix,3,2);
    addEdge(adjMatrix,1,3);
    addEdge(adjMatrix,3,1);
    addEdge(adjMatrix,3,4);
    addEdge(adjMatrix,4,3);
    addEdge(adjMatrix,1,4);
    addEdge(adjMatrix,4,1);

    printAdjMatrix(adjMatrix);

    return 0;
}
