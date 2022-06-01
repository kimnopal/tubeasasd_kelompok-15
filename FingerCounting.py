import cv2
import time

# definisi lebar dan tinggi kamera
wCam, hCam = 640, 480

# membuat video object dan memilih kamera pada parameter
cap = cv2.VideoCapture(0)

# men-set lebar dan tinggi kamera
cap.set(3, wCam)
cap.set(4, hCam)

while True:
    # membuat/membaca frame kamera
    success, img = cap.read()

    # merender img/video dan menajalankan kamera
    cv2.imshow("Image", img)
    # untuk memberikan delay 1ms
    cv2.waitKey(1)