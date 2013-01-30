#include <stdio.h>

int gcd(int a , int b)
{
	if (b==0)
		return a;
	gcd( b, a%b);
}

int  main()
{
	printf("%d\r\n",gcd(36,24));

}
