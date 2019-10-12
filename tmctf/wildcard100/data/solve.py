from PIL import Image
import numpy as np
import wave
import struct
import math
import scipy.ndimage
import os
import IPython

num_pixels = 30

seen = {}

for f in os.listdir('.'):
    if f is not '.' and f is not '..':
        png = Image.open(f)
        array = np.asarray(png)
        IPython.embed()


# modify rgba array
# img = PIL.Image.fromarray(array)
# img.show()
# img.save('<directory>')
