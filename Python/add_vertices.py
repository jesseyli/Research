import networkx as nx
from PIL import Image, ImageDraw

G = nx.Graph()
imageName = input('Enter image name: ')
img = Image.open(imageName)
img = img.split()[0]

index = 0
data = list(img.getdata())

for i in data:
	if i == 100 or i == 200:
		xy =  (index % img.size[1], index // img.size[0])
		G.add_node(index,coord = xy)
	index += 1

data = G.nodes()
print(data)


