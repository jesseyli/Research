from PIL import Image, ImageDraw

imageName = input('Enter image name: ')
img = Image.open(imageName)
dim = img.size
degrees = int(input('Enter number of degrees per slice, must be a factor of 360: '))

def draw_circle(size, d):
	# Draws a circle divided into equal slices.  Each size is d degrees of the
	# original circle.  The outputted image has dimensions size.
	
	circle = Image.new('L',size)
	draw = ImageDraw.Draw(circle)
	slices = 360//d
	color = 100
	curr_d = 0
	for i in range(0,slices):
		color = 300 - color
		draw.pieslice((0,0,size[0],size[1]),i*d,i*d,
			None,color)

	return circle

circle = draw_circle(dim, degrees)
overlay = Image.new('L',dim)
for i in range(0,dim[0]):
	for j in range(0,dim[1]):
		#finish for loop that adds the two images together
