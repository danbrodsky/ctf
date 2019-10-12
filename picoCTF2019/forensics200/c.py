from PIL import Image
import numpy as np

img1 = Image.open('./cattos.jpg')

img2 = Image.open('./kitters.jpg')
array1 = np.asarray(img1)
array2 = np.asarray(img2)
# modify rgba array

array = np.subtract(array2, array1)
img = Image.fromarray(array)
img.show()
img.save("./diff.jpg")

