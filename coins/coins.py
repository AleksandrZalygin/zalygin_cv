from skimage.measure import label
from skimage.morphology import binary_closing, binary_dilation, binary_opening, binary_erosion
import matplotlib.pyplot as plt
import numpy as np


def area(LB, label=1):
    return np.sum(LB == label)


LB = np.zeros((16, 16))
LB[4:, :4] = 2

LB[3:10, 8:] = 1
LB[[3, 4, 3], [8, 8, 9]] = 0
LB[[8, 9, 9], [8, 8, 9]] = 0
LB[[3, 4, 3], [-2, -1, -1]] = 0
LB[[9, 8, 9], [-2, -1, -1]] = 0

LB[12:-1, 6:9] = 3

image = np.load("coins.npy.txt")
labeled = label(image)

coins = {}
for i in range(1, labeled.max() + 1):
    a = area(labeled, i)
    if a not in coins:
        coins[a] = 0
    coins[a] += 1


nominals = [1,2,5,10]
summa = 0
for i, count in enumerate(sorted(coins)):
    summa += coins[count] * nominals[i]

print(summa)

