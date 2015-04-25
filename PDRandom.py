#!/usr/bin/env python
import math
import random
import sys
#Generate Random Numbers according to a probability density function
# 
#
#By Ken Leung


# the probility density need to return value >=0 
 
class PDRandom:
	mFunc=None
	mNumSubDiv=10
	#public

	#return one random Number
	def Next(self):
		while True:
			if self.mDimension > 1:
				randNum=[random.random() for d in range(self.mDimension)]
				(divIndex,values) = self.getX(randNum)
				if (self.acceptReject(divIndex,values)):
					return values
				

			else:

				randNum = random.random()
				(divIndex,x) = self.getX(randNum)
				if (self.acceptReject(divIndex,x)):
					return x

	#return a list of random numbers
	def RandList(self,num=1):
		temp=[]
		for i in range(num):
			temp.append(self.Next()) 
		return temp


	#return a (number, count) list
	# 
	# if   binLowerBound <= randomNum < binLowerBound + binWidth, randomNum will be counted for this bin with value = binLowerBound
	#inclusive lowerbound, exclusive upper
	def GetCountList(self,binWidth, li):
		if self.mDimension > 1:
			totalBins = []
			allBins = 1
			countlist=[]

			for d in range(self.mDimension):
				totalBins.append(int(math.ceil((self.mUpper[d]-self.mLower[d])/binWidth[d])))
				allBins= allBins * totalBins[d]
			for i in range(allBins):
				eachIndex = self.getEachIndex(i,totalBins)
				temp =[self.mLower[d] + binWidth[d] * eachIndex[d] for d in range(self.mDimension)] 
				temp.append(0)
				countlist.append(temp)
			for item in li:
				binIndex=[]
				for d in range(self.mDimension):
					binIndex.append(int((item[d] - self.mLower[d])/binWidth[d]))
				globalIndex = self.getGlobalIndex(binIndex,totalBins)
				countlist[globalIndex][self.mDimension] = countlist[globalIndex][self.mDimension]  + 1
			return countlist


				




		else:
			totalBins = int(math.ceil((self.mUpper-self.mLower) /binWidth))
			countlist =[ (self.mLower+ binWidth *i, 0) for i in range(totalBins)]
			for item in li:
				binIndex = int((item- self.mLower)/binWidth)
				countlist[binIndex] =(countlist[binIndex][0], countlist[binIndex][1]+1)

			return countlist

	# output to a file with space speration format
	def OutputCountList(self,countlist, filename):
		with open(filename,"w") as f :

			if self.mDimension > 1 :
				for item in countlist:
					for i in range(len(item)):
						item[i] = str(item[i])
					line = " ".join(item)
					f.write(line+"\n")

					

			else:
				for tup in countlist:
					line = "%f %d\n"%(tup[0],tup[1])
					f.write(line)
			
			print "Sucess: output to %s"%filename










	# some helper function
	# subdiv: used for finding max in a division
	# divWidth too small -> performance hit
	# divWidth too large -> rejection rate increase -> performance hit
	def __init__(self,func,lower,upper , divWidth, subdiv=1000, dimension=1):
		self.mDimension=dimension
		if dimension > 1:
			try:
				assert isinstance(lower,list)
				assert isinstance(upper,list)
				assert isinstance(divWidth,list)
				
			except AssertionError:
				sys.stderr.write("not pass a list argument for dimension %d"%(dimension))
				exit(1)
			self.mFunc = func 
			self.mLower =lower
			self.mUpper =upper
			self.mDivWidth = divWidth

			if not isinstance(subdiv,list):
				subdiv = subdiv ** (1.0/dimension)
				subdiv = math.ceil(subdiv)
				self.mNumSubDiv = [int(subdiv) for i in range(dimension)]
				#print self.mNumSubDiv
			else:
				self.mNumSubDiv= [int(num) for num in subdiv ]

			self.mNumDiv=[]
			self.mTotalNumDiv =1 
			for i in range(dimension):
				numDiv = (upper[i] - lower[i]) /divWidth[i]

				numDiv = math.ceil(numDiv)
				numDiv= int(numDiv)
				self.mTotalNumDiv =self.mTotalNumDiv  * numDiv
				self.mNumDiv.append(numDiv)

			#print self.mNumDiv
			
			#print self.mTotalNumDiv
			self.mMaxs=[]
			for globalIndex in range(self.mTotalNumDiv):
				eachIndex = self.getEachIndex(globalIndex,self.mNumDiv)
				#print eachIndex
				subLower=[i*divWidth[index]+lower[index] for index, i in enumerate(eachIndex)]

				subUpper= [(i+1)*divWidth[index] +lower[index]  for index, i in enumerate(eachIndex)]
			#	print subLower
			#	print subUpper
				self.mMaxs.append(self.findMax(subLower, subUpper))

			#print self.mMaxs
			self.initMapping()	


		else: # dimension =1

			self.mFunc = func 
			self.mLower =lower
			self.mUpper =upper
			self.mDivWidth = divWidth
			self.mNumSubDiv=int(subdiv)

			numDiv = (upper - lower) /divWidth
			numDiv = math.ceil(numDiv)
			numDiv= int(numDiv)
			self.mNumDiv =numDiv
			self.mMaxs=[ self.findMax(i*divWidth+lower, (i+1)*divWidth +lower) for i in range(numDiv)]
			self.initMapping()

	# finding the local max of a function by discrete method
	def findMax(self, low, upper):

		if (self.mDimension > 1):
			maximum =-1
			divWidth= [float(upper[i] - low[i])/self.mNumSubDiv[i] for i in range(self.mDimension)]
		
			totalNumSubDiv = 1
			numValuePoints= [self.mNumSubDiv[d]+1 for d in range(self.mDimension)]
			for d in range(self.mDimension):
				totalNumSubDiv = totalNumSubDiv * (numValuePoints[d])


			for i in range (totalNumSubDiv):
				values =[]
				eachIndex = self.getEachIndex(i,numValuePoints) 
			
				for d in range(self.mDimension):		
					values.append(eachIndex[d] *divWidth[d] + low[d] )
				temp=self.mFunc(values)	
		
				if i == 0:
					maximum=temp
					continue

				if temp > maximum:
					maximum=temp	


			return maximum
			





		else:
			maximum =-1
			divWidth = float(upper-low)/self.mNumSubDiv
			#print divWidth
			for i in range (self.mNumSubDiv+1):
				temp=self.mFunc(divWidth*i+low)	
				if i == 0:
					maximum=temp
					continue

				if temp > maximum:
					maximum=temp	

	#		print maximum
			return maximum

	# init the mapping of random number	to our range
	def initMapping(self): 
		if self.mDimension > 1:
			areas = []
			groupAreas=[]
			self.mMapValues=[]
			
			totalArea=[]
			tempNum =  1
			for d in range(self.mDimension):
				totalArea.append([0 for i in range(tempNum)])
				tempNum = self.mNumDiv[d] * tempNum
				groupAreas.append([0 for i in range(tempNum	)])
				self.mMapValues.append([None for i in range(tempNum)])


			for i in range(len(self.mMaxs)):
				temp = self.mMaxs[i]
				for d in range(self.mDimension):
					temp = temp * self.mDivWidth[d]
				areas.append(temp)

				#== 
				eachIndex = self.getEachIndex(i, self.mNumDiv)
				for d in range(self.mDimension):
					# total Area
					if d ==0:
						totalArea[d][0] = totalArea[d][0] + temp
						
					else:
						subEachIndex = []
						subNumDiv =[]
						for d2 in range(d):
							subEachIndex.append(eachIndex[d2])
							subNumDiv.append(self.mNumDiv[d2])
						subGlobalIndex =self.getGlobalIndex(subEachIndex, subNumDiv)
						totalArea[d][subGlobalIndex] = totalArea[d][subGlobalIndex] + temp
					#=========group Area ==============
					subEachIndex=[]
					subNumDiv=[]
					for d2 in range(d+1):
						subEachIndex.append(eachIndex[d2])
						subNumDiv.append(self.mNumDiv[d2])
					subGlobalIndex =self.getGlobalIndex(subEachIndex, subNumDiv)
					groupAreas[d][subGlobalIndex] = groupAreas[d][subGlobalIndex] + temp


			
			

			

			
			
			for d in range(self.mDimension):
				for totalIndex, total in enumerate(totalArea[d]):
					if d == 0:
						tempArea = 0
						for index, area in enumerate( groupAreas[d]):
							lowerBound = tempArea
							tempArea = tempArea+area
							self.mMapValues[d][index]=((index,lowerBound/total, area/total))
					else:
						subGlobalIndex = totalIndex 
						subNumDiv=[]
						for d2 in range(d):
							subNumDiv.append(self.mNumDiv[d2])
						subEachIndex = self.getEachIndex(subGlobalIndex,subNumDiv)
						subEachIndex.append(0)
						subNumDiv.append(self.mNumDiv[d])
						tempArea = 0 
						for ownIndex in range (self.mNumDiv[d]):
							subEachIndex[d]=ownIndex
							tempGlobalIndex = self.getGlobalIndex(subEachIndex,subNumDiv)
							lowerBound =tempArea
							tempArea = tempArea + groupAreas[d][tempGlobalIndex]
							self.mMapValues[d][tempGlobalIndex]=((ownIndex,lowerBound/total, groupAreas[d][tempGlobalIndex]/total ))

			print self.mMapValues				
			return 	




			#================
			for  area in enumerate(areas):
				lowerBound = tempArea
				tempArea = tempArea+area
				self.mMapValues.append ( (index,lowerBound/totalArea,area/totalArea))
			self.mMapValues= sorted(self.mMapValues,key = lambda mapping:mapping[2],reverse =True )

		else:
			#===================D - 1 =======================
			areas =[]
			totalArea=0
			for i in range(len(self.mMaxs)):
				temp = self.mMaxs[i] * self.mDivWidth
				totalArea = totalArea + temp
				areas.append(temp)
		#	print areas
			tempArea =0.0
			self.mMapValues=[]
			for index, area in enumerate(areas):
				lowerBound = tempArea
				tempArea = tempArea+area
				self.mMapValues.append ( (index,lowerBound/totalArea,area/totalArea))

			self.mMapValues= sorted(self.mMapValues,key = lambda mapping:mapping[2],reverse =True )
			print self.mMapValues	

	#given a rand, return the corresponding x value 
	def getX (self,rand):

#		print rand
		if self.mDimension >1 :
			values=[]
			eachIndex =[]
			eachDiv =[]
			globalIndex=0
			for d, ran in enumerate(rand):
				
				if d == 0:
					for  (divIndex,lower, width) in self.mMapValues[d]:
						if ran >= lower and ran < (lower + width):
							tempWidth = ran -lower
							
							values.append(self.mLower[d]+(divIndex+(tempWidth/width)) * self.mDivWidth[d])
							eachIndex.append(divIndex) 
							eachDiv.append(self.mNumDiv[d])

							break
				else:
					eachIndex.append(0)
					eachDiv.append(self.mNumDiv[d])
					for ownIndex in range(self.mNumDiv[d]):
						eachIndex[d]= ownIndex
						globalIndex = self.getGlobalIndex(eachIndex,eachDiv)
						(divIndex,lower, width) = self.mMapValues[d][globalIndex]
						if ran >= lower and ran < (lower + width):
							tempWidth = ran -lower
							values.append(self.mLower[d]+ (divIndex+(tempWidth/width)) * self.mDivWidth[d])
							
							break

				

			#print values
			return  (globalIndex, values)



		else :
			for  (divIndex,lower, width) in self.mMapValues:
				if rand >= lower and rand < (lower + width):
					tempWidth = rand -lower
	#				print str(tempWidth) + " " + str(lower)
					return (divIndex,self.mLower+(divIndex+(tempWidth/width)) * self.mDivWidth )

			print "error: corresponding x not found"

	def acceptReject(self,divIndex, x):
		randHight = random.random() * self.mMaxs[divIndex]
		funcH = self.mFunc(x) 
		if randHight <= funcH:
			#print "accept: funcH %f v.s. randHight %f"%(funcH,randHight)
			return True
		else:

			#print "reject: funcH %f v.s. randHight %f"%(funcH,randHight)
			return False


	# used for dimension > 1
	def getEachIndex(self,globalIndex, numDiv):
		eIndex=[]
		for d in range(len(numDiv)):
			index = globalIndex% numDiv[d]
			globalIndex= globalIndex - index
			globalIndex = int(globalIndex/numDiv[d])
			eIndex.append(index)
		return eIndex

	def getGlobalIndex(self,eachIndex, numDiv):
		globalIndex = 0	
		for i in range(len(eachIndex)-1,-1, -1):
			if i == 0:
				globalIndex = globalIndex + eachIndex[i]
			else:
				globalIndex = (globalIndex + eachIndex[i]) * numDiv[i-1]

		return globalIndex





# end of class ========================

if __name__=="__main__":

	def test(i):
		summ = 1.0/(2*math.pi)**0.5 *math.exp(-((i)**2)/2.0)
		#summ= abs(i)
		return summ

	a = PDRandom(test,-5 ,5 ,0.5,dimension=1)
	li=a.RandList(50000)
	#ran = random.random()
	#li= a.RandList(50000)
	#print li
	countlist=a.GetCountList(0.1,li)
	#print countlist


	#print li
	#print countlist
	a.OutputCountList(countlist, "result")

