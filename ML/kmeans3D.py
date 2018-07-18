import numpy as np
import tensorflow as tf
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Debug and output config
# # Remove TensorFlow output for GPU blabla
os.environ["TF_CPP_MIN_LOG_LEVEL"]="2"
# # Print full content of numpy array
np.set_printoptions(threshold=np.nan)

# Initialization
num_points = 1000
dimensions = 3
points=np.empty([num_points,dimensions],dtype=float)
points[:,0] = np.random.triangular(50,75,130,num_points)  #Weight
points[:,1] = np.random.triangular(18,40,105,num_points)  #Age
points[:,2] = 70*np.random.random_sample(num_points)+130  #Height

def translate_colors(tab):
    ret=np.empty(tab.size,dtype='U30')
    for i in range(tab.size):
        if tab[ i ] % 10 == 0:
            ret[ i ] = "black"
        elif tab[ i ] % 10 == 1:
            ret[ i ] = "blue"
        elif tab[ i ] % 10 == 2:
            ret[ i ] = "green"
        elif tab[ i ] % 10 == 3:
            ret[ i ] = "red"
        elif tab[ i ] % 10 == 5:
            ret[ i ] = "violet"
        elif tab[ i ] % 10 == 6:
            ret[ i ] = "pink"
        elif tab[ i ] % 10 == 7:
            ret[ i ] = "dimgrey"
        elif tab[ i ] % 10 == 8:
            ret[ i ] = "yellow"
        elif tab[ i ] % 10 == 9:
            ret[ i ] = "cyan"
        else:
            ret[i] = "White"
    return ret

# Return a tensor of 1 epoch (number of times the tensor will be evaluated)
def input_fn():
    return tf.train.limit_epochs(tf.convert_to_tensor(points, dtype=tf.float32), num_epochs=1)

# Kmeans Estimator definition
num_clusters = 15
kmeans = tf.contrib.factorization.KMeansClustering(num_clusters=num_clusters, use_mini_batch=False)


# train
num_iterations = 30
for _ in range(num_iterations):
    kmeans.train(input_fn)
    cluster_centers = kmeans.cluster_centers ()
    print('Training ... score:', kmeans.score(input_fn))


# map the input points to their clusters
cluster_indices = list(kmeans.predict_cluster_index(input_fn))

# print results to stdout
for i, point in enumerate(points):
    print("point = ", point," cluster =", cluster_indices[i])
#    center = cluster_centers[cluster_index]
#    print('point:', point, 'is in cluster', cluster_index, 'centered at', center)


# plotting results into a nice 3D graph
fig = plt.figure()
ax = Axes3D(fig)
sc=ax.scatter3D(xs=points[:,0], ys=points[:,1], zs=points[:,2], c=translate_colors(np.asarray(cluster_indices)), s=15, marker='H')
ax.set_xlabel('Weight')
ax.set_ylabel('Age')
ax.set_zlabel('Height')
plt.show()

