from PIL import Image, ImageDraw

imageName = input('Enter image name: ')
img = Image.open(imageName)
img = img.split()[0]
circle = Image.new('L',img.size)

index = 0
draw = ImageDraw.Draw(circle)
draw.pieslice((0,0,circle.size[0],circle.size[1]),0,45,None,100)
draw.pieslice((0,0,circle.size[0],circle.size[1]),90,135,None,200)
data = list(img.getdata())
print(len(data))