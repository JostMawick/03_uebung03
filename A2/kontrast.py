import matplotlib.pyplot as plt
img = plt.imread('boats_low_contrast.pgm')
plt.imshow(img, cmap='gray', vmin=0, vmax=255)
plt.axis('off')
plt.show()