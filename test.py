import PDRandom
import math

def cosine (input):
	return abs(math.cos(input))
def sine(input):
	return abs(math.sin(input[0])*math.sin(input[1]))
def sine3(input):
	return abs(math.sin(input[0])*math.sin(input[1])*math.sin(input[2]))

#gen = PDRandom.PDRandom(sine3, [-1,0,1], [math.pi,math.pi,math.pi], [10,10,10],dimension=3)
#lis = gen.RandList(1000)
#print (gen.GetCountList([10,10,10], lis))
#gen.OutputGenCountList(100000,[50,50,50],"sine3")
gen = PDRandom.PDRandom(cosine, -1, math.pi, 10,dimension=1)
#gen.OutputGenCountList(100000,50,"consine2")
gen.multiOutputRawRandom(1000000,"hi",1)

