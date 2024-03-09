from skimage.measure import label
from skimage.morphology import binary_closing, binary_dilation, binary_opening, binary_erosion
import matplotlib.pyplot as plt
import numpy as np
import os

for n, image_path in enumerate(os.listdir("wires_images"), 1):
    print(f"\nКартинка №{n}: ")
    image = np.load("wires_images/" + image_path)

    labeled_image = label(image)
    for i in range(1, labeled_image.max() + 1):
        wire = labeled_image == i
        result = binary_erosion(wire, np.ones((3, 1)))
        count_parts = label(result).max()
        if count_parts == 0:
            print(f'Провода {i} нет!')
        elif count_parts == 1:
            print(f'У провода {i} нет отверстий')
        else:
            print(f"Провод {i} порван на {count_parts}")
