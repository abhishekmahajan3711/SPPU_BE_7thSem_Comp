

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


n=int(input('Enter number till which you want a fibonacci series'))

fib=[]
for i in range(n):
    fib.append(0)

for i in range(n):
    print(fib[i])

#recursive
def fibn(i,fib):
    if(i<=1):
        return i
    elif(fib[i]):
         return fib[i]
    else:
        fib[i]=fibn(i-1,fib)+fibn(i-2,fib)
        return fib[i]
        
fibn(n-1,fib)

for i in range(n):
    print(fib[i])

#non-recursive


# print(0)

# a=0
# b=1
# for i in range(0,n-1):
#     c=a+b
#     print(c)
#     a=b
#     b=c
