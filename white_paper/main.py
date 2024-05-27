import cv2
import numpy as np
import zmq

cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Image1", cv2.WINDOW_GUI_NORMAL)

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")

cam = cv2.VideoCapture(0)

lower_threshold = 200
upper_threshold = 255


def update_lower_threshold(value):
    global lower_threshold
    lower_threshold = value


def update_upper_threshold(value):
    global upper_threshold
    upper_threshold = value


cv2.createTrackbar("Lower Threshold", "Mask", lower_threshold, 255, update_lower_threshold)
cv2.createTrackbar("Upper Threshold", "Mask", upper_threshold, 255, update_upper_threshold)


def add_text_with_perspective(image, text, contour):
    rect = cv2.minAreaRect(contour)
    box = np.intp(cv2.boxPoints(rect))

    cx = int(rect[0][0])
    cy = int(rect[0][1])
    angle = rect[2]

    rows, cols = image.shape[:2]
    M = cv2.getRotationMatrix2D((cx, cy), angle, 1)
    rotated = cv2.warpAffine(image, M, (cols, rows))

    white_paper = np.ones_like(rotated) * 255

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (0, 0, 0)
    thickness = 2
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = int((cols - text_size[0]) / 2)
    text_y = int((rows + text_size[1]) / 2)
    cv2.putText(white_paper, text, (text_x, text_y), font, font_scale, font_color, thickness, cv2.LINE_AA)

    result = cv2.addWeighted(rotated, 1, white_paper, 0.5, 0)

    return result


while cam.isOpened():
    ret, frame = cam.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    _, threshold = cv2.threshold(blurred, lower_threshold, upper_threshold, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 5000]

    cv2.drawContours(frame, large_contours, -1, (0, 0, 255), 5)
    if large_contours:
        image_with_text = add_text_with_perspective(frame, "Hello world", large_contours[0])
        cv2.imshow("Image1", image_with_text)

    cv2.imshow("Image", frame)
    cv2.imshow("Mask", threshold)

    if cv2.waitKey(10) == ord("q"):
        break

cv2.destroyAllWindows()
