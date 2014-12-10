'''
A prototype of separable SVM, 2-dimensional case
'''
import matplotlib.pyplot as plt
import random

#The X coordinate of support vectors (Category 1)
SupportVectorsX1 = [50, 0]
SupportVectorsY1 = [0, 50]
SupportVectorsX2 = [50]
SupportVectorsY2 = [50]

#For simplicity, assume margin plane will not be vertical.
k = 0.0
b1 = 0.0
b2 = 0.0

#If support two of the support vectors are of category 1
if len(SupportVectorsX1) == 2:
	k = (SupportVectorsY1[0] - SupportVectorsY1[1])*1.0/(SupportVectorsX1[0] - SupportVectorsX1[1])
else:
	k = (SupportVectorsY2[0] - SupportVectorsY2[1])*1.0/(SupportVectorsX2[0] - SupportVectorsX2[1])

b1 = SupportVectorsY1[0] - k*SupportVectorsX1[0]
b2 = SupportVectorsY2[0] - k*SupportVectorsX2[0]

#Draw the hyperplane.
XLeft = -999
XRight = 999
XLeftBound = -200
XRightBound = 200
YLowBound = -200
YHighBound = 200

MarginX = [XLeft, XRight]
MarginY1 = [XLeft*k+b1, XRight*k+b1]
MarginY2 = [XLeft*k+b2, XRight*k+b2]

plt.plot(SupportVectorsX1,SupportVectorsY1, 'ro')
plt.plot(MarginX, MarginY1, 'ro-')
plt.plot(SupportVectorsX2,SupportVectorsY2, 'b*')
plt.plot(MarginX, MarginY2, 'b*-')
plt.axis([XLeftBound,XRightBound,YLowBound,YHighBound])

def BelongToCategory1(x,y):
	#You want the points to be above margin plane of category 1
	if b1 > b2:
		if y > k*x+b1:
			return True
		else:
			return False
	else:
		if y < k*x+b1:
			return True
		else:
			return False

def BelongToCategory2(x,y):
	#You want the points to be above margin plane of category 2
	if b2 > b1:
		if y > k*x+b2:
			return True
		else:
			return False
	else:
		if y < k*x+b2:
			return True
		else:
			return False

#Randomly create points with restriction of support vectors.
NumPoints = 9000
currNumPoints = 0
SampleX1 = []
SampleY1 = []
SampleX2 = []
SampleY2 = []
while currNumPoints <= NumPoints:
	x = random.uniform(XLeftBound, XRightBound)
	y = random.uniform(YLowBound, YHighBound)
	if BelongToCategory1(x,y):
		SampleX1.append(x)
		SampleY1.append(y)
		currNumPoints += 1
	elif BelongToCategory2(x,y):
		SampleX2.append(x)
		SampleY2.append(y)
		currNumPoints += 1
		
# plt.plot(SampleX1, SampleY1, 'ro')
# plt.plot(SampleX2, SampleY2, 'b*')

#==============================================
#Sample Compression begin, here assume the hyper plane direction is unchanged, and the relative height of two hyper planes are unchanged
maxX1 = -999
maxY1 = -999
minX2 = 999
minY2 = 999
#the two points which is the max in x and the max in y in category 1
MaxXPoint1 = []
MaxYPoint1 = []
MaxXPoint2 = []
MaxYPoint2 = []
for i in xrange(0,len(SampleX1)):
	if SampleX1[i] > maxX1:
		maxX1 = SampleX1[i]
		MaxXPoint1 = [SampleX1[i], SampleY1[i]]
	if SampleY1[i] > maxY1:
		maxY1 = SampleY1[i]
		MaxYPoint1 = [SampleX1[i], SampleY1[i]]

for i in xrange(0,len(SampleX2)):
	if SampleX2[i] < minX2:
		minX2 = SampleX2[i]
		MaxXPoint2 = [SampleX2[i], SampleY2[i]]
	if SampleY2[i] < minY2:
		minY2 = SampleY2[i]
		MaxYPoint2 = [SampleX2[i], SampleY2[i]]


#Plot the compression plane of category 1, plot the compression plane of category 2
plt.plot([MaxXPoint1[0], MaxYPoint1[0]], [MaxXPoint1[1], MaxYPoint1[1]], 'ro--')
plt.plot([MaxXPoint2[0], MaxYPoint2[0]], [MaxXPoint2[1], MaxYPoint2[1]], 'bo--')

kCompression1 = (MaxYPoint1[1]-MaxXPoint1[1])*1.0/(MaxYPoint1[0]-MaxXPoint1[0])
kCompression2 = (MaxYPoint2[1]-MaxXPoint2[1])*1.0/(MaxYPoint2[0]-MaxXPoint2[0])
bCompression1 = MaxYPoint1[1] - kCompression1*MaxYPoint1[0]
bCompression2 = MaxYPoint2[1] - kCompression2*MaxYPoint2[0]

RemainingPoints = 0
RemainX1 = []
RemainY1 = []
RemainX2 = []
RemainY2 = []

for i in xrange(0,len(SampleX1)):
	x = SampleX1[i]
	y = SampleY1[i]
	if y > kCompression1*x+bCompression1:
		RemainX1.append(x)
		RemainY1.append(y)
		RemainingPoints += 1

for i in xrange(0,len(SampleX2)):
	x = SampleX2[i]
	y = SampleY2[i]
	if y < kCompression2*x+bCompression2:
		RemainX2.append(x)
		RemainY2.append(y)
		RemainingPoints += 1

print "Remain points / total points = "
print RemainingPoints*1.0/NumPoints

plt.plot(RemainX1, RemainY1, 'ro')
plt.plot(RemainX2, RemainY2, 'b*')

plt.show()