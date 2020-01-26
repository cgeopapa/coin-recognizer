from numpy import cos, sin, zeros, argwhere, arange, pi, array, abs
from scipy import ndimage
from _collections import defaultdict
from PIL import ImageDraw

def grayscale(im):
    grayscale=zeros((len(im), len(im[0])))
    for x in range(len(im)-1):
        for y in range(len(im[0])-1):
            grayscale[x, y] = im[x, y, 0] *.25 + im[x, y, 1] *.5 + im[x, y, 2] *.25
    return grayscale


def hough_circles(im):
    [rmin, rmax] = [35, 55]
    steps = 100
    threshold = 0.4
    edges = []
    for e in argwhere(im > 200):
        edges.append(e[::-1])

    points = []
    for r in range(rmin, rmax, 2):
        for t in range(steps):
            points.append((r, int(r * cos(2 * pi * t / steps)), int(r * sin(2 * pi * t / steps))))
    acc = defaultdict(int)
    for x, y in edges:
        for r, dx, dy in points:
            a = x - dx
            b = y - dy
            acc[(a, b, r)] += 1
    maxVote = max(acc.values())
    threshold = int(maxVote*threshold)
    print("Acc DONE")

    circles = []
    for k, v in sorted(acc.items(), key=lambda i: -i[1]):
        x, y, r = k
        if v >= threshold and all((x - xc) ** 2 + (y - yc) ** 2 > rc ** 2 for xc, yc, rc in circles):
            circles.append((x, y, r))
    print("Circles DONE")

    return circles

def sobel(im):
    Gx = array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    Gy = array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    Gxx = ndimage.convolve(im, Gx)
    Gyy = ndimage.convolve(im, Gy)

    G = abs(Gxx) + abs(Gyy)
    return G
