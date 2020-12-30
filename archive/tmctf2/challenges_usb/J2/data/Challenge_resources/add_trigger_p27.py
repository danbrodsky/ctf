"""
 This script for python2.7
 A backend server add a teigger which you submitted to validation images.
 Please check where it is added:).
"""

import sys
import os
import numpy as np
import scipy.misc
import glob

def add_filter(name1, name2, name3):
    # Original image
    image1 = scipy.misc.imread(name1)
    # Filter image
    image2 = scipy.misc.imread(name2)
    image3 = np.copy(image1)
    w = image2.shape[1]
    h = image2.shape[0]
    for y in range(h):
        for x in range(w):
            image3[y+148,x+148,:] = image2[y,x,:]
    scipy.misc.imsave(name3+name1.replace(sys.argv[1],""), image3)

if __name__ == '__main__':
    # args 
    #1. Directory path of validation files
    #2. Trigger image path
    #3. Output dir path
    #ex)python add_trigger_p27.py validation_img/ trigger.jpg trigger_output/tmp/
    filepaths = glob.glob(sys.argv[1]+"*")
    trigger = sys.argv[2]
    output = sys.argv[3]
    if not os.path.exists(output):
        os.mkdir(output)
    for fname in filepaths:
        add_filter(fname, trigger, output)
