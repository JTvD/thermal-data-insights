import cv2
import numpy as np
from matplotlib import pyplot as plt

# Create a histogram plot of the pixel values and temperature values
# plotting opencv histograms
# https://docs.opencv.org/master/d1/db7/tutorial_py_histogram_begins.html

if __name__ == "__main__":
    filename = "test_data/test"
    img = cv2.imread(filename + ".png")

    # Subplot 1, the image
    axs = plt.subplot(2, 2, 1)  # 2x2 grid, pos 1
    plt.imshow(img)
    axs.set_title('Image')

    # Subplot 2, a histogram of the colors in the image.
    # this does not say much for a thermal image
    axs = plt.subplot(2, 2, 2)  # 2x2 grid, pos 2
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(histr, color=col)
        plt.axis(xmin=0, xmax=256, ymin=0)
    axs.set_title('Histogram of image')
    axs.set_xlabel('Pixel value')
    axs.set_ylabel('Occurance')

    # Subplot 3, a histogram of the temperature values in the csv
    temp_vals = np.loadtxt(filename + ".csv", delimiter=',')

    # Numpy histogram is a lot faster than matplot
    axs = plt.subplot(2, 1, 2)  # 2x1 grid, pos 2: bottom
    bins = int((temp_vals.max() - temp_vals.min()) * 10)
    frequency, bins = np.histogram(temp_vals, bins=256, range=[temp_vals.min(),
                                                               temp_vals.max()])
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    axs.bar(center, frequency, align='center', width=width)
    # #plt.hist(temp_vals, bins=256)
    axs.set_title('Histogram of temperature')
    axs.set_xlabel('Temperature')
    axs.set_ylabel('Occurance')

    # Show all plots
    # fig.tight_layout()
    mng = plt.get_current_fig_manager()  # Full screen
    mng.window.state('zoomed')
    plt.savefig(f'histogram of {filename}.png')
    plt.show()
