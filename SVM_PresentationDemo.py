from SVMSampleCompression import *

def ConnectTwoPoints(p1, p2, lineSolid = True, lineColor = 'k', figure = 3):
	plt.figure(figure)
	if lineSolid == True:
		plt.plot([p1.x, p2.x], [p1.y,p2.y], lineColor)
	else:
		plt.plot([p1.x, p2.x], [p1.y,p2.y], 'k--')

def getK(p1, p2):
	k = (p1.y-p2.y)*1.0/(p1.x-p2.x)
	return k

def getB(p1, p2):
	k = getK(p1, p2)
	b = p1.y-k*p1.x
	return b

def getCrossPoint(k1, k2, b1, b2,label):
	x = (b1-b2)*1.0/(k2-k1)
	y = k1*x+b1
	return Point(x,y,label)

def drawDiamonds(points):
	#Sample Compression begin, here assume the hyper plane direction is unchanged, and the relative height of two hyper planes are unchanged
	pMaxXClass1 = Point(-999,0, True)
	pMinXClass1 = Point(999,0, True)
	pMaxYClass1 = Point(0,-999, True)
	pMinYClass1 = Point(0,999, True)

	pMaxXClass2 = Point(-999,0, False)
	pMinXClass2 = Point(999,0, False)
	pMaxYClass2 = Point(0,-999,False)
	pMinYClass2 = Point(0,999,False)

	pMiddleClass1 = Point(0,0,True)
	pMiddleClass2 = Point(0,0,False)

	plt.figure(4)
	for point in points:
		if point.label == True:
			plt.plot(point.x, point.y, 'ro')
		else:
			plt.plot(point.x, point.y, 'b*')

	plt.figure(3)
	for point in points:
		if point.label == True:
			plt.plot(point.x, point.y, 'ro')
		else:
			plt.plot(point.x, point.y, 'b*')

	for point in points:
		if point.label == True:
			if point.x > pMaxXClass1.x:
				pMaxXClass1 = point
			if point.x < pMinXClass1.x:
				pMinXClass1 = point
			if point.y > pMaxYClass1.y:
				pMaxYClass1 = point
			if point.y < pMinYClass1.y:
				pMinYClass1 = point						
		else:
			if point.x > pMaxXClass2.x:
				pMaxXClass2 = point
			if point.x < pMinXClass2.x:
				pMinXClass2 = point
			if point.y > pMaxYClass2.y:
				pMaxYClass2 = point	
			if point.y < pMinYClass2.y:
				pMinYClass2 = point	

	# k1Class1 = getK(pMaxYClass1,pMinYClass1)
	# k2Class1 = getK(pMaxXClass1,pMinXClass1)
	# b1Class1 = getB(pMaxYClass1,pMinYClass1)
	# b2Class1 = getB(pMaxXClass1,pMinXClass1)
	# pMiddleClass1 = getCrossPoint(k1Class1, k2Class1, b1Class1, b2Class1,True)

	# k1Class2 = getK(pMaxYClass2,pMinYClass2)
	# k2Class2 = getK(pMaxXClass2,pMinXClass2)
	# b1Class2 = getB(pMaxYClass2,pMinYClass2)
	# b2Class2 = getB(pMaxXClass2,pMinXClass2)
	# pMiddleClass2 = getCrossPoint(k1Class2, k2Class2, b1Class2, b2Class2, False)


	ConnectTwoPoints(pMaxXClass1, pMaxYClass1, lineColor = 'k')
	ConnectTwoPoints(pMaxXClass1, pMinYClass1, lineColor = 'k')
	ConnectTwoPoints(pMinXClass1, pMinYClass1, lineColor = 'k')
	ConnectTwoPoints(pMinXClass1, pMaxYClass1, lineColor = 'k')

	ConnectTwoPoints(pMaxXClass2, pMaxYClass2, lineColor = 'k')
	ConnectTwoPoints(pMaxXClass2, pMinYClass2, lineColor = 'k')
	ConnectTwoPoints(pMinXClass2, pMinYClass2, lineColor = 'k')
	ConnectTwoPoints(pMinXClass2, pMaxYClass2, lineColor = 'k')

	# ConnectTwoPoints(pMaxXClass1, pMinXClass1, False,lineColor = 'k')
	# ConnectTwoPoints(pMaxYClass1, pMinYClass1, False,lineColor = 'k')
	# ConnectTwoPoints(pMaxXClass2, pMinXClass2, False,lineColor = 'k')
	# ConnectTwoPoints(pMaxYClass2, pMinYClass2, False,lineColor = 'k')

	# ConnectTwoPoints(pMiddleClass1, pMiddleClass2, False,lineColor = 'k')

compression = SVMSampleCompression()
compression.CreateAndDrawRandomPoints()
compression.FirstOrderCompress()	
drawDiamonds(compression.samplePoints)
plt.show()
