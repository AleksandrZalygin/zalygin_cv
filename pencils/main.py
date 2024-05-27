import numpy as np
import cv2

total_pencils = 0
for image_index in range(1, 13):
    pencil_count = 0
    image_path = f"images/images/img ({image_index}).jpg"
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    _, binary_image = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY)
    eroded_image = cv2.erode(binary_image, None, iterations=40)
    inverted_image = cv2.bitwise_not(eroded_image)

    mask = np.zeros(inverted_image.shape, dtype="uint8")

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(inverted_image, 4, cv2.CV_32S)

    for label_index in range(1, num_labels):
        x, y, w, h = stats[label_index, cv2.CC_STAT_LEFT], stats[label_index, cv2.CC_STAT_TOP], stats[label_index, cv2.CC_STAT_WIDTH], stats[label_index, cv2.CC_STAT_HEIGHT]
        area = stats[label_index, cv2.CC_STAT_AREA]
        cX, cY = centroids[label_index]

        if 500000 < area < 700000:
            pencil_count += 1
            total_pencils += 1

    print(f"In picture {image_index}, there are {pencil_count} pencils")

print(f"There are {total_pencils} pencils in all the pictures")
