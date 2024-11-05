

n=int(input("Enter number of terms to be shown : "))

def Fib(n,a,b,step):
	if(n==1):
		return step
	else:
		c=a+b
		print(c)
		return Fib(n-1,b,c,step+1)

if(n==0):
	print("no series for 0 input")
else:	
	print(0)	
	step=Fib(n,0,1,1)
	print("Step count : ",step)

