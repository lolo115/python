import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
import sys
import os

def get_cmap(n):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    #colors = [(0, 0, 0), (1, 0, 0), (0.0, 0.5, 0.0), (0.75, 0.75, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]
    colors = ['k','m','b','g','y','r','w']
    cm=mpl.colors.LinearSegmentedColormap.from_list('cmlolo', colors, N=100)
    return plt.cm.get_cmap(cm, n)


def main():
    N = 100
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.axis('scaled')
    ax.set_xlim([0, N])
    ax.set_ylim([-0.5, 0.5])
    cmap = get_cmap(N)
    for i in range(N):
        rect = plt.Rectangle((i, -0.5), 1, 1, facecolor=cmap(i))
        ax.add_artist(rect)
    ax.set_yticks([])
    plt.show()


if __name__ == '__main__':
    main()

    # df = pd.DataFrame(np.random.randint(37, 46, size=(100, 1)), columns=['SIZE'])
    # n=np.array([1, 2, 3])
    # print(n.shape)
    # df2 = pd.DataFrame(np.random.rand(100, 1), columns=['LO'])
    # #print(df)
    # #print(df2)
    # df3=df.join(df2)
    # print(df3)
    # print(cm.hot(0.1))

