import PDRandom
import math

def cosine (input):
	return abs(math.cos(input))
def sine(input):
	return abs(math.sin(input[0])*math.sin(input[1]))


gen = PDRandom.PDRandom(sine, [0,0], [math.pi,math.pi], [10,10],dimension=2)
lis = gen.RandList(1000)
print (gen.GetCountList([10,10], lis))

gen.OutputGenCountList(500000,[50,50],"sine2")