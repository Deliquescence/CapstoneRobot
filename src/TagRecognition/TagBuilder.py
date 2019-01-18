import numpy as np
import opencv, PIL
from opencv import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd




aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
fig = plt.figure();
for i in range(1,4):
    ax = fig.add_subplot(ny,nx, i)
    img = aruco.drawMarker(aruco_dict,i,700)
    plt.imshow(img, cmap = mpl.cmg.gray, interpolation = "nearest")
    ax.axis("off")
    
plt.savefig("_data/markers.pdf")
plt.show() 
