from PIL import Image, ImageDraw
import ast, math

#imageName = input('Enter image name: ')
imageName = 'nocenter.tif'  #remove later
img = Image.open(imageName)
img = img.split()[0]
dim = img.size
#center = ast.literal_eval(input('Enter location of center (x,y): '))
center = (336,386) #remove later
#degrees = int(input('Enter number of degrees per slice, factor of 360 for best results: '))
degrees = 45 #remove later



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
	color = 100

	x2 = center[0]
	y2 = center[1]

	for i in range(0,slices):
		color = 300-color
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
	return circle


circle = draw_circle(dim, degrees, center)
overlay = Image.new('L',dim)
for i in range(0,dim[0]):
	for j in range(0,dim[1]):
		overlay.putpixel((i,j),min(255,img.getpixel((i,j))+circle.getpixel((i,j))))

overlay.show()