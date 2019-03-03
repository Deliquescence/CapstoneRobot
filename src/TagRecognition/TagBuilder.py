import numpy as np
import cv2
import PIL
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import math


def generate_single():
    aruco_dict = aruco.Dictionary_create(1, 3)
    img = aruco.drawMarker(aruco_dict, 0, 1000)

    fig = plt.figure()
    fig.set_size_inches(10, 10)

    plt.imshow(img, cmap=plt.get_cmap("gray"), interpolation="nearest")
    plt.axis('off')

    plt.savefig("img/CustomDict_3x3_1/tag.png")
    plt.show()


def show_n(n: int):
    # https://docs.opencv.org/3.4.0/d9/d6a/group__aruco.html#gac84398a9ed9dd01306592dd616c2c975
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)

    fig = plt.figure()

    for i in range(n):
        square_len = math.ceil(math.sqrt(n))
        ax = fig.add_subplot(square_len, square_len, i+1)
        img = aruco.drawMarker(aruco_dict, i, 700)
        plt.imshow(img, cmap=plt.get_cmap("gray"), interpolation="nearest")
        ax.axis("off")

    # plt.savefig("_data/markers.pdf")
    plt.show()


if __name__ == '__main__':
    generate_single()
    # show_n(16)
