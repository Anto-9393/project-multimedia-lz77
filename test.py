#
#
#
# 
from image import * 
from PIL import Image
import numpy as np 


image = Image.open("im2.jpg")
data = np.array(image)
arr = data.flatten()
a = data
#delta_encode(a)
#delta_decode(b)
path = "./im3.jpg"
lz77Compress (path,500,500)
lz77Decompressor()


