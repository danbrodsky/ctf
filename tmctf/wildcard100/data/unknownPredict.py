from scipy.misc import imread, imresize
import numpy as np
import os
import hashlib
import matplotlib.pyplot as plt
from IPython import embed

#perform the prediction
from keras.models import load_model
model = load_model('cnn.h5')

seen = {}

unknown = []

dist = []

three_six = [0,0]
c= 0

# images =['15263.jpg', '3629.jpg', '23752.jpg', '18505.jpg', '27945.jpg', '6268.jpg', '1800.jpg', '31908.jpg', '10935.jpg', '23439.jpg', '28033.jpg', '27537.jpg', '227.jpg', '3967.jpg', '23288.jpg', '1981.jpg', '1498.jpg', '29964.jpg', '19176.jpg', '672.jpg', '2241.jpg', '23046.jpg', '314.jpg', '17580.jpg', '21951.jpg', '1570.jpg', '26577.jpg', '10692.jpg', '7621.jpg', '17059.jpg', '10117.jpg', '8503.jpg', '22244.jpg', '19842.jpg', '31015.jpg', '8892.jpg', '21544.jpg', '21539.jpg', '21249.jpg', '25302.jpg', '28521.jpg', '22790.jpg', '19500.jpg', '22960.jpg', '32670.jpg', '31783.jpg', '33016.jpg', '15180.jpg', '490.jpg', '15507.jpg', '29412.jpg', '6260.jpg', '14223.jpg', '32983.jpg', '18888.jpg', '7494.jpg', '29178.jpg', '7009.jpg', '2094.jpg', '10153.jpg', '24500.jpg', '17875.jpg', '28109.jpg', '33841.jpg', '24718.jpg', '28025.jpg', '13635.jpg', '31330.jpg', '30633.jpg', '30945.jpg', '28494.jpg', '30758.jpg', '2108.jpg', '24441.jpg', '33845.jpg', '12835.jpg', '32863.jpg', '5369.jpg', '8037.jpg', '21879.jpg', '25902.jpg', '31524.jpg', '2424.jpg', '5269.jpg', '3642.jpg', '26348.jpg', '16894.jpg', '28132.jpg', '11971.jpg', '28992.jpg', '20403.jpg', '32756.jpg', '10763.jpg', '9283.jpg', '692.jpg', '29955.jpg', '3484.jpg', '17808.jpg', '21739.jpg', '30867.jpg', '27284.jpg', '15749.jpg', '7823.jpg', '32058.jpg', '31115.jpg', '29526.jpg', '11592.jpg', '5194.jpg', '7744.jpg', '26001.jpg', '21403.jpg', '32689.jpg', '20767.jpg', '15347.jpg', '31406.jpg', '28606.jpg', '19376.jpg', '30217.jpg', '29216.jpg', '4189.jpg', '26000.jpg', '6993.jpg', '31974.jpg', '21463.jpg', '13088.jpg', '19629.jpg', '26520.jpg', '25563.jpg', '4679.jpg', '8663.jpg', '8351.jpg', '7211.jpg', '27501.jpg', '27313.jpg', '27064.jpg', '4380.jpg', '2537.jpg', '22793.jpg', '29986.jpg', '30920.jpg']

images = ['3347.jpg', '12849.jpg']

# for f in images:
for f in os.listdir('.'):
    c +=1
    print(c)
    if f.endswith('.jpg'):
        x = imread(f,mode='L')
        #compute a bit-wise inversion so black becomes white and vice versa
        #x = np.invert(x)
        #make it the right size
        x = imresize(x,(28,28))

        #convert to a 4D tensor to feed into our model
        x = x.reshape(1,28,28,1)
        x = x.astype('float32')
        x /= 255

        hashx = hashlib.md5(np.array_str(x).encode('utf-8')).hexdigest()
        if hashx not in seen.keys():
            seen[hashx] = True

            out = model.predict(x)[0]
            # print(out)
            # print(out)
            # print(c)
            # print(out[3])
            # print(out[6])
            # print(f)

            dist.append(out[3]-out[6])
            if out[3] - out[6] > 0.1*out[3]:
                three_six[0] += 1
            elif out[3] - out[6] < -0.1*out[6]:
                three_six[1] += 1
            else:
                unknown.append(f)
            # else:
            #     print("FUCKKKKKKKKK")
            #     print(f)
            #     break
        else:
            print(f)

#np.histogram(dist)
# _ = plt.hist(dist, bins='auto')
# plt.show()
# embed()
print(three_six[0])
print(three_six[1])
print(unknown)

