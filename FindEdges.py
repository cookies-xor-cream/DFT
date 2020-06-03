#Edge Detection Algorithm

from PIL import Image, ImageColor
from math import floor
import csv

fidelity = 1

downscale = 2.5
threshold = 60

grayweight = 1

rweight = 1
gweight = 1
bweight = 1

cyanweight= 1
magweight = 1
yelweight = 1

#Opens the image, w and h are the dim
im = Image.open("JessicaRabbit.jpg")
px = im.load()
im.close()
w, h = im.size

w //= downscale
h //= downscale

w = floor(w)
h = floor(h)

print(w,h)

#The list is of the right size
pxCol = [[0]*w for i in range(h)]

for i in range(0, w-1):
    for j in range(0, h-1):
        gray = 0
        cyan = 0
        mag = 0
        yel = 0
        
        for n in range(3):
            gray += abs(px[downscale*i, downscale*j][n]*grayweight/3)
            
            if n != 0:
                cyan += abs(px[downscale*i, downscale*j][n]*cyanweight/2)
            
            if n != 1:
                mag += abs(px[downscale*i, downscale*j][n]*magweight/2)
            
            if n != 2:
                yel += abs(px[downscale*i, downscale*j][n]*yelweight/2)
                
        gray = abs(int(gray))
        
        cyan = abs(int(cyan))
        mag = abs(int(mag))
        yel = abs(int(yel))
            
        r = abs(int(px[downscale*i, downscale*j][0]*rweight))
        g = abs(int(px[downscale*i, downscale*j][1]*gweight))
        b = abs(int(px[downscale*i, downscale*j][2]*bweight))
        
        contrast = max([r,g,b,cyan,mag,yel,gray])
        pxCol[j][i] = [contrast, 1]
    
edges = []
    
for j in range(1, h-2):
    for i in range(1, w-2):
        c0 = abs(pxCol[j][i][0] - pxCol[j][i+1][0])
        c1 = abs(pxCol[j][i][0] - pxCol[j+1][i][0])
        
        contrast_list = [c0, c1]
        contrast = max(contrast_list)
        
        if contrast > threshold:
            edges.append([i,j, pxCol[j][i][1]])
#             edges.append([i*downscale,j*downscale])


with open("edges_white_backdrop.csv", mode = "w") as dp:
    dp.truncate()
    dpLog = csv.writer(dp, lineterminator = "\n", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    for i in range(0, len(edges)-1, fidelity):
        dpLog.writerow(edges[i])
        
print(len(edges)//fidelity)