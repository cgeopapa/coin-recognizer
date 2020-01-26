from PIL import Image, ImageDraw
import numpy
import utils as u
import cv2
from time import time

i = int(input("Which image should I analyze?(Give a number from 1-6)\n"))
i=(i-1)%6
images = ['examples/coins002.tif',
          'examples/coins003.tif',
          'examples/coins004.tif',
          'examples/coins005.tif',
          'examples/coins006.tif',
          'examples/coins008.tif']
imageName = images[i]

start = time()
imarray = cv2.imread(imageName)

imarray = u.grayscale(imarray)
print("Grayscale DONE")
imarray = cv2.GaussianBlur(imarray, (5, 5), cv2.BORDER_DEFAULT)
print("Blur DONE")
imarray = u.sobel(imarray)
print("Sobel DONE")

circles = u.hough_circles(imarray)

out = cv2.imread(imageName)
for x, y, r in circles:
    cv2.circle(out, (x, y), r, (255, 0, 0), 2)
    coin = "This is a coin"
    if r in range(35, 40):
        coin = "10c"
    elif r in range(40, 48):
        coin = "1e"
    elif r in range(48, 50):
        coin = "50c"
    else:
        coin = "2e"
    cv2.putText(out, coin, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

print("Found {} coins \nIn {} sec".format(len(circles), time() - start))
cv2.imshow('image',out)
cv2.waitKey(0)
cv2.destroyAllWindows()
