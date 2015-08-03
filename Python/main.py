from PIL import Image, ImageDraw
import ast, math

# Use a branch treshold for how many pixels to travel before counting as branching
# may not need to use branching if angle is sufficiently small
# currently doesn't work for 1 degree increment, not enough colors with 8 bit

#imageName = input('Enter image name: ')
imageName = 'nocenter.tif'  #remove later
img = Image.open(imageName)
img = img.split()[0]
dim = img.size
#center = ast.literal_eval(input('Enter location of center (x,y): '))
center = (310,305) #remove later
#degrees = int(input('Enter number of degrees per slice, factor of 360 for best results: '))
degrees = 18 #remove later



'''
def draw_circle(size, d, center):
	# Draws a circle centered at center divided into equal slices.  Each slice is
	# d degrees of the original circle.  The outputted image has dimensions size.
	
	circle = Image.new('L',size)
	radii = min(size[0] - center[0],size[1] - center[0],size[1] - center[1],size[1] - center[0])
	draw = ImageDraw.Draw(circle)
	slices = 360//d
	color = 100
	for i in range(0,slices):
		color = 300 - color
		draw.pieslice((center[0]-radii,center[1]-radii,center[0]+radii,center[1]+radii),i*d,i*d,
			None,color)

	return circle
'''
def draw_circle(size, d, center):
	# Draws a circle centered at center divided into equal slices.  Each slice is
	# d degrees of the original circle.  The outputted image has dimensions size.
	
	circle = Image.new('L',size)
	radii = min(size[0] - center[0],size[1] - center[0],size[1] - center[1],size[1] - center[0])
	draw = ImageDraw.Draw(circle)
	slices = 360//d
	color = 0

	x2 = center[0]
	y2 = center[1]

	for i in range(0,slices):
		color += 1
		radians=d*i*math.pi/180;
		x1=radii*math.cos(radians) + x2;
		y1=radii*math.sin(radians) + y2;

		# thickness of line
		thick = 1

		# compute angle
		a = math.pi/2
		if x1 != x2: 
			a = math.atan((y2-y1)/(x2-x1))
		sin = math.sin(a)
		cos = math.cos(a)
		xdelta = sin * thick / 2.0
		ydelta = cos * thick / 2.0
		xx1 = x1 - xdelta
		yy1 = y1 + ydelta
		xx2 = x1 + xdelta
		yy2 = y1 - ydelta
		xx3 = x2 + xdelta
		yy3 = y2 - ydelta
		xx4 = x2 - xdelta
		yy4 = y2 + ydelta
		draw.polygon((xx1, yy1, xx2, yy2, xx3, yy3, xx4, yy4),color,None)	
	return circle,color 


circle,last_color = draw_circle(dim, degrees, center)
overlay = Image.new('L',dim)
start = {}   # start is a dictionary with colors as labels and points as entries
for i in range(1,last_color + 1):
	start[i] = []

for i in range(0,dim[0]):
	for j in range(0,dim[1]):
		color = min(255,img.getpixel((i,j))+circle.getpixel((i,j)))
		overlay.putpixel((i,j),color)
		if color > 0 and color < 255:
			start[color].append((i,j))

def ends(start, img, color):
	start_color = img.getpixel(start)
	s5 = list(start)
	s1 = (s5[0]-1,s5[1]-1)
	s2 = (s5[0],s5[1]-1)
	s3 = (s5[0]+1,s5[1]-1)
	s4 = (s5[0]-1,s5[1])
	s6 = (s5[0]+1,s5[1])
	s7 = (s5[0]-1,s5[1]+1)
	s8 = (s5[0],s5[1]+1)
	s9 = (s5[0]+1,s5[1]+1)
	if start_color == color:
		return start
	if start_color != 255 and start_color != 1:
		img.putpixel(start,255)
		return ends(s1,img,color) + ends(s2,img,color) + ends(s3,img,color) + ends(s4,img,color) + ends(s6,img,color) + ends(s7,img,color) + ends(s8,img,color) + ends(s9,img,color)
	return ()
	
def distance(xcoord1, xcoord2, ycoord1, ycoord2):
	deltax=math.pow((xcoord2-xcoord1), 2)
	deltay=math.pow((ycoord2-ycoord1), 2)
	distanceA=math.sqrt(deltax+deltay)
	return distanceA


def lawOfCosines(point1,point2,center):
	xcoord1 = point1[0]
	xcoord2 = point2[0]
	originX = center[0]
	ycoord1 = point1[1]
	ycoord2 = point2[1]
	originY = center[1]
	distanceA=distance(xcoord1, xcoord2, ycoord1, ycoord2)
	distanceB=distance(xcoord2, originX, ycoord2, originY)
	distanceC=distance(xcoord1, originX, ycoord1, originY)
	aSquared=math.pow(distanceA,2)
	bSquared=math.pow(distanceB,2)
	cSquared=math.pow(distanceC,2)
	cosAng=((cSquared-aSquared-bSquared)/(-2*distanceA*distanceB))
	angRad=math.acos(cosAng)
	angDeg=(180*angRad)/math.pi
	return angDeg


x = center[0]
y = center[1]
angles = []

while x < dim[0]:
	value = overlay.getpixel((x,y)) 
	if not(value == 0 or value == 255):
		overlay.putpixel((x,y),0)
		e = ends((x,y),overlay,2)
		if e != ():
			angles.append(lawOfCosines((x,y),e,center))
	x += 1

i = 2
while i < last_color:
	i += 1
	for j in start[i-1]:
		e = ends(j,overlay,i)
		if e != ():
			angles.append(lawOfCosines(j,e,center))
for j in start[last_color]:
	e = ends(j,overlay,1)
	if e != ():
		angles.append(lawOfCosines(j,e,center))

overlay.show()
print(len(angles))
#for i in start:
#	print(i,start[i])

'''
//get results from table and measure angle
originX=254;
originY=281;
angles=newArray();

for(i=0;i<1374;i+=2){
	xcoord1=getResult("X",i);
	xcoord2=getResult("X",i+1);
	ycoord1=getResult("Y",i);
	ycoord2=getResult("Y",i+1);
	distanceA=distance(xcoord1, xcoord2, ycoord1, ycoord2);
	distanceB=distance(xcoord2, originX, ycoord2, originY);
	distanceC=distance(xcoord1, originX, ycoord1, originY);
	angle=lawOfCosines(distanceA, distanceB, distanceC);
	print(angle);
}

'''
