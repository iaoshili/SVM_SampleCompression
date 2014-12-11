'''
A prototype of separable SVM sample compression, 2-dimensional case
'''
import matplotlib.pyplot as plt
import random
from Point import *

XLeftBound = -200
XRightBound = 200
YDownBound = -200
YUpBound = 200

class SVMSampleCompression:
	def __init__(self):
		#SV1 and SV2 should be on the same margin plane.
		self.SV1 = Point(50,0,True)
		self.SV2 = Point(0,50,True)

		self.SV3 = Point(50,50,False)

		self.kMargin = (self.SV1.y-self.SV2.y)*1.0/(self.SV1.x-self.SV2.x)
		self.b1Margin = self.SV1.y - self.kMargin*self.SV1.x
		self.b2Margin = self.SV3.y - self.kMargin*self.SV3.x

		self.samplePoints = []

		self.DrawLine(self.kMargin,self.b1Margin, lineColor = 'r')
		self.DrawLine(self.kMargin,self.b2Margin, lineColor = 'b')

	#Randomly create points restricted by support vectors
	def CreateAndDrawRandomPoints(self):
		NumPoints = 900

		currNumPoints = 0
		while currNumPoints <= NumPoints:
			x = random.uniform(XLeftBound,XRightBound)
			y = random.uniform(YDownBound,YUpBound)
			newPoint = Point(x,y,True)
			if self.LabelPositive(x,y):
				newPoint.label = True
				self.samplePoints.append(newPoint)
				currNumPoints += 1
			elif self.LabelNegative(x,y):
				newPoint.label = False
				self.samplePoints.append(newPoint)
				currNumPoints += 1

		plt.figure(1)
		plt.axis([XLeftBound,XRightBound,YDownBound,YUpBound])

		for point in self.samplePoints:
			if point.label == True:
				plt.plot(point.x, point.y, 'ro')
			else:
				plt.plot(point.x, point.y, 'b*')

	#Given two points, draw a line.
	def DrawLinePoint(self, p1, p2, lineSolid = True, lineColor = 'k', figure = 1):
		if p1.x == p2.x:
			raise Exception("Vertical line currently not supported")

		k = (p2.y-p1.y)*1.0/(p2.x-p1.x)
		b = p1.y - k*p1.x
		self.DrawLine(k,b,lineSolid,lineColor,figure)

	def DrawLine(self,k,b,lineSolid = True, lineColor = 'k', figure = 1):
		plt.figure(figure)
		p1 = Point(-999, -999*k+b,True)
		p2 = Point(999, 999*k+b, True)

		if lineSolid:
			plt.plot([p1.x, p2.x], [p1.y,p2.y], lineColor)
		else:
			plt.plot([p1.x, p2.x], [p1.y,p2.y], 'k--')

		# #Draw the hyperplane.
		# XLeft = -999
		# XRight = 999
		# XLeftBound = -200
		# XRightBound = 200
		# YLowBound = -200
		# YHighBound = 200

		# MarginX = [XLeft, XRight]
		# MarginY1 = [XLeft*k+b1, XRight*k+b1]
		# MarginY2 = [XLeft*k+b2, XRight*k+b2]

		# plt.plot(SupportVectorsX1,SupportVectorsY1, 'ro')
		# plt.plot(MarginX, MarginY1, 'ro-')
		# plt.plot(SupportVectorsX2,SupportVectorsY2, 'b*')
		# plt.plot(MarginX, MarginY2, 'b*-')
		# plt.axis([XLeftBound,XRightBound,YLowBound,YHighBound])

	def LabelPositive(self, x,y):
		#You want the points to be above margin plane of category 1
		if self.b1Margin > self.b2Margin:
			if y > self.kMargin*x+self.b1Margin:
				return True
			else:
				return False
		else:
			if y < self.kMargin*x+self.b1Margin:
				return True
			else:
				return False

	def LabelNegative(self,x,y):
		#You want the points to be above margin plane of category 2
		if self.b2Margin > self.b1Margin:
			if y > self.kMargin*x+self.b2Margin:
				return True
			else:
				return False
		else:
			if y < self.kMargin*x+self.b2Margin:
				return True
			else:
				return False

	def FirstOrderCompress(self):
		RemainingPoints = []
		RemainingPointNum = 0

		#Sample Compression begin, here assume the hyper plane direction is unchanged, and the relative height of two hyper planes are unchanged
		pMaxXClass1 = Point(-999,0, True)
		pMaxYClass1 = Point(0,-999, True)
		pMinXClass2 = Point(999,0, False)
		pMinYClass2 = Point(0,999,False)

		for point in self.samplePoints:
			if point.label == True:
				if point.x > pMaxXClass1.x:
					pMaxXClass1 = point
				if point.y > pMaxYClass1.y:
					pMaxYClass1 = point			
			else:
				if point.x < pMinXClass2.x:
					pMinXClass2 = point
				if point.y < pMinYClass2.y:
					pMinYClass2 = point				

		self.DrawLinePoint(pMaxXClass1, pMaxYClass1,lineSolid = False)
		self.DrawLinePoint(pMinXClass2, pMinYClass2,lineSolid = False)

		kCompression1 = (pMaxXClass1.y - pMaxYClass1.y)*1.0/(pMaxXClass1.x - pMaxYClass1.x)
		kCompression2 = (pMinXClass2.y - pMinYClass2.y)*1.0/(pMinXClass2.x - pMinYClass2.x)
		bCompression1 = pMaxXClass1.y - kCompression1*pMaxXClass1.x
		bCompression2 = pMinXClass2.y - kCompression2*pMinXClass2.x

		for point in self.samplePoints:			
			x = point.x
			y = point.y
			if point.label == True and y > kCompression1*x+bCompression1:
				RemainingPoints.append(point)
				RemainingPointNum += 1
			if point.label == False and y < kCompression2*x+bCompression2:
				RemainingPoints.append(point)
				RemainingPointNum += 1

		plt.figure(2)
		for point in RemainingPoints:
			if point.label == True:
				plt.plot(point.x, point.y, 'ro')
			else:
				plt.plot(point.x, point.y, 'b*')


	# #Plot the compression plane of category 1, plot the compression plane of category 2
	# plt.plot([MaxXPoint1[0], MaxYPoint1[0]], [MaxXPoint1[1], MaxYPoint1[1]], 'ro--')
	# plt.plot([MaxXPoint2[0], MaxYPoint2[0]], [MaxXPoint2[1], MaxYPoint2[1]], 'bo--')


	# RemainingPoints = 0
	# RemainX1 = []
	# RemainY1 = []
	# RemainX2 = []
	# RemainY2 = []



	# print "Remain points / total points = "
	# print RemainingPoints*1.0/NumPoints

	# plt.plot(RemainX1, RemainY1, 'ro')
	# plt.plot(RemainX2, RemainY2, 'b*')

	# plt.show()