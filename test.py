import PDRandom
import math
def cosine (input):
		return abs(math.cos(input))
def sine(input):
	return abs(math.sin(input[0])*math.sin(input[1]))
def sine3(input):
	return abs(math.sin(input[0])*math.sin(input[1])*math.sin(input[2]))

def paraboloid(input):
	return input[0]**2 + input[1]**2

def inverseExp(input):
	return math.exp(-input)
def cos2(input):
	return abs(math.cos(input[0])*math.cos(input[1]))

if __name__ == '__main__':
	

	#gen = PDRandom.PDRandom(sine3, [-1,0,1], [math.pi,math.pi,math.pi], [10,10,10],dimension=3)
	#lis = gen.RandList(1000)
	#print (gen.GetCountList([10,10,10], lis))
	#gen.OutputGenCountList(100000,[50,50,50],"sine3")
	#gen = PDRandom.PDRandom(cosine, -1, math.pi, 10,dimension=1)
	#gen.OutputGenCountList(100000,50,"consine2")
	#gen.OutputRawRandom(1000000,"hi",nproc=2)
	#gen = PDRandom.PDRandom(paraboloid,[-5,-5],[5,5],[10,10],dimension=2)
	#gen.OutputGenCountList(1000000,[100,100],"paraboloid")
	gen = PDRandom.PDRandom(inverseExp,0,10,10)
	#gen.OutputGenCountList(int(10009),1000,"inverse_exp",nproc=4)
	#temp=gen.RandList(int(1e6),nproc=4)
	#print (gen.GetCountList(10,temp))
	#gen.OutputRawRandom(1000,"append",nproc=4,foption='a')
	#gen.OutputRawRandom(1000,"append",nproc=1,foption='a')
	

	gen=PDRandom.PDRandom(cos2,[-math.pi,-math.pi],[math.pi,math.pi],[10,10],dimension=2)
	#gen.OutputGenCountList(int(10001),[200,200],"cosine2",nproc=4)
	#gen.OutputRawRandom(1000,"append2",nproc=4,foption='a')
	#gen.OutputRawRandom(1000,"append2",nproc=4,foption='a')
	gen.OutputGenCountList(int(1e6),[100,100],"cosine2",nproc=4,foption='a')	
	

