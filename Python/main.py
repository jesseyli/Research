from PIL import Image, ImageDraw
import ast, math

imageName = input('Enter image name: ')
img = Image.open(imageName)
img = img.split()[0]
dim = img.size
center = ast.literal_eval(input('Enter location of center (x,y): '))
degrees = int(input('Enter number of degrees per slice, factor of 360 for best results: '))

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

circle = draw_circle(dim, degrees, center)
overlay = Image.new('L',dim)
for i in range(0,dim[0]):
	for j in range(0,dim[1]):
		overlay.putpixel((i,j),min(255,img.getpixel((i,j))+circle.getpixel((i,j))))

overlay.show()