import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def get_cmap():
    colors = ['k','m','b','g','y','r','w']
    colmap=mpl.colors.LinearSegmentedColormap.from_list('cmlolo', colors, N=100)
    return plt.cm.get_cmap(colmap, 100)

if __name__=='__main__':
    input_colors=['k','m','b','g','y','r','w']
    nb=10
    r=np.random.rand(1000)
    print(r.shape)
    mycm=get_cmap()
    print(mycm(0.1))

    random_colors=np.random.choice(input_colors, nb, p=[0.4, 0.2, 0.05, 0.05, 0.2, 0.07, 0.03])
    random_colors_df=pd.DataFrame(random_colors, columns=['COLOR'])

    size_df=pd.DataFrame(np.random.randint(37, 46, size=(nb, 1)), columns=['SIZE'])

    src_df=random_colors_df.join(size_df)
    print(src_df)

    x=src_df.groupby(['COLOR','SIZE']).size().to_frame('cnt').reset_index()
    print(x)