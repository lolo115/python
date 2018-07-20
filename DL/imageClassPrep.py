# https://github.com/kylemcdonald/SmileCNN

import os
import numpy as np
from skimage.measure import block_reduce
from skimage.io import imread


root_dir='D:/JetBrains_projects/PycharmProjects/work/'
os.chdir(root_dir)
#negative_paths = list(list_all_files(root_dir+'SMILEsmileD-master/SMILEs/negatives/negatives7/', ['.jpg']))
#print('loaded', len(negative_paths), 'negative examples')
#positive_paths = list(list_all_files('SMILEsmileD-master/SMILEs/positives/positives7/', ['.jpg']))
#print 'loaded', len(positive_paths), 'positive examples'
negative_list = []
for file in [pos for pos in os.listdir('SMILEsmileD-master/SMILEs/negatives/negatives7/')
if pos.endswith(".jpg")]:
	negative_list.append('SMILEsmileD-master/SMILEs/negatives/negatives7/'+file)

positive_list = []
for file in [pos for pos in os.listdir('SMILEsmileD-master/SMILEs/positives/positives7/')
if pos.endswith(".jpg")]:
	positive_list.append('SMILEsmileD-master/SMILEs/positives/positives7/'+file)

examples = [(path, 0) for path in negative_list] + [(path, 1) for path in positive_list]

def examples_to_dataset(examples, block_size=2):
    X = []
    y = []
    z = []
    for path, label in examples:
        # On passe les images en N/B pour etre conforme au modèle d'apprentissage
        img = imread(path, as_gray=True)
        # Les images étant en 64/64 on les réduit en 32/32
        img = block_reduce(img, block_size=(block_size, block_size), func=np.mean)
        X.append(img)
        y.append(label)
        z.append(path)
    return np.asarray(X), np.asarray(y), np.asarray(z,str)

X, y , z = examples_to_dataset(examples)
X = X.astype(np.float32) / 255.
y = y.astype(np.int32)
print(X.dtype, X.min(), X.max(), X.shape)
print(y.dtype, y.min(), y.max(), y.shape)

X = np.expand_dims(X, axis=-1)
np.save('X.npy', X)
np.save('y.npy', y)
np.save('z.npy',z)
