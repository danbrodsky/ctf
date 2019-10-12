from scipy.misc import imread, imresize
import numpy as np
import os
import hashlib

#perform the prediction
from keras.models import load_model
model = load_model('cnn.h5')

seen = {}

unknown = []

three_six = [0,0]
c= 0
for f in os.listdir('.'):
    c +=1
    print(c)
    if f.endswith('.jpg'):
        x = imread(f,mode='L')
        #compute a bit-wise inversion so black becomes white and vice versa
        x = np.invert(x)
        #make it the right size
        x = imresize(x,(28,28))
        #convert to a 4D tensor to feed into our model
        x = x.reshape(1,28,28,1)
        x = x.astype('float32')
        x /= 255

        hashx = hashlib.md5(','.join(str(item) for innerlist in x for item in innerlist).encode('utf-8')).hexdigest()
        if hashx not in seen.keys():
            seen[hashx] = True

            out = model.predict(x)[0]
            #print(out)
            # print(c)
            if out[4] - out[7] > 0.0000001:
                three_six[0] += 1
            elif out[4] - out[7] < -0.0000001:
                three_six[1] += 1
            else:
                unknown.append(f)
            # else:
            #     print("FUCKKKKKKKKK")
            #     print(f)
            #     break

print(three_six[0])
print(three_six[1])
print(unknown)

