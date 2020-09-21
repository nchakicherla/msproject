from skimage import data, io, filters
import matplotlib
import numpy as np
import matplotlib.pyplot as plot

image = io.imread('crop.jpg')



sobel = filters.sobel(image)

#io.imshow(sobel)
#io.show()



io.imsave("sobel.jpg", sobel)
print(sobel)

for a in sobel:
    for b in a.all():
        if np.sqrt(b) > 0.1:
            print(b)
