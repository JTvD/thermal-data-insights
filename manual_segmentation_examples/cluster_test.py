import numpy as np
import cv2
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt


# Attempt one: Clustering
# The background color is not uniform, which might pose a problem...
# https://towardsdatascience.com/k-means-clustering-one-rule-to-group-them-all-f47e00720ee7


if __name__ == "__main__":
    filename = "test_data/test"
    img = cv2.imread(filename + ".png")
    height, width, _ = img.shape

    temp_vals = np.loadtxt(filename + ".csv", delimiter=',')
    one_d_array = temp_vals.flatten('C').reshape(-1, 1)
    clt = KMeans(n_clusters=2)
    clt.fit(one_d_array)
    temp_mask = clt.labels_
    temp_mask = temp_mask.reshape(height, width)
    print("here")

    # Subplot 1, the image
    axs = plt.subplot(1, 2, 1)  # 1x2 grid, pos 1: left
    plt.imshow(img)
    axs.set_title('Image')

    # Subplot 2, mask
    axs = plt.subplot(1, 2, 2)  # 1x2 grid, pos 2: right
    plt.imshow(temp_mask)
    axs.set_title('K means mask')

    # plt.savefig(f'histogram of {filename}.png')
    plt.show()
