# https://github.com/kylemcdonald/SmileCNN

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.measure import block_reduce
from skimage.io import imread

from keras.models import model_from_json

root_dir='D:/JetBrains_projects/PycharmProjects/work/'
os.chdir(root_dir)

model = model_from_json(open('model.json').read())
model.load_weights('weights.h5')


def print_indicator(data, model, class_names, bar_width=50):
    probabilities = model.predict(np.array([data]))[0]
    print(probabilities)
    left_count = int(probabilities[1] * bar_width)
    right_count = bar_width - left_count
    left_side = '-' * left_count
    right_side = '-' * right_count
    print(class_names[0], left_side + 'XXX' + right_side, class_names[1])


#X = np.load('X.npy')
#y = np.load('y.npy')
#z = np.load('z.npy')
class_names = ['Neutral', 'Smiling']
#for idx,img in enumerate(X):
#    if (idx%500 == 0):
#        print_indicator (img, model, class_names)
#        print ('label = ', z[ idx ])
#        image=mpimg.imread(z[idx])
#        plt.imshow(image)
#        plt.show()


img = imread(root_dir+'smile_32x32.jpg', as_gray=True)
print(img.shape)
# Nécessaire pour se mettre en conformité avec le format en entrée du modèle
img_model=np.expand_dims(img,axis=2)

print_indicator(img_model,model,class_names)
plt.imshow(img)
plt.show()
