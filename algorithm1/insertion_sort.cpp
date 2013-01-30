#include <stdio.h>

void insertion_sort( int* data, int num)
{
	int key;
	for(int i = 1; i < num ;i++)
	{	
		for(int k = i ; k >= 0 ; k--)
		{
			if( data[i])
		}
	}
}


int main()
{
	int a[6]= {8,2,4,9,3,6};
	for(int i = 0 ; i < 6; i++)
	{
		printf("%d ",a[i]);
	}
	printf("\r\n");
	insertion_sort(a,6);
	for(int i = 0 ; i < 6; i++)
	{
		printf("%d ",a[i]);
	}
	printf("\r\n");
}
