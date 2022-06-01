import cv2
import time
import os
import HandTrackingModule as htm

# definisi lebar dan tinggi kamera
wCam, hCam = 640, 480

# membuat video object dan memilih kamera pada parameter
cap = cv2.VideoCapture(0)

# men-set lebar dan tinggi kamera
cap.set(3, wCam)
cap.set(4, hCam)

# mengambil semua nama foto
folderPath = "images"
myList = os.listdir(folderPath)

# mengambil semua path foto
overlayList = []
for imPath in myList:
    # mengimport foto
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

pTime = 0

# instansiasi class
detector = htm.handDetector(detectionCon=0.75)

# list kumpulan titik ujung jari 
tipIds = [4, 8, 12, 16, 20]

while True:
    # membuat/membaca frame kamera
    success, img = cap.read()

    # membuat img/video baru yang sudah mendeteksi tangan
    img = detector.findHands(img)

    lmList = detector.findPosition(img, draw=False)
    
    # mengecek apakah ada tangan yang terdeteksi
    if len(lmList) != 0:
        # list untuk menampung jari mana saja yang membuka
        fingers = []

        # mengecek jempol
        # membandingkan sumbu x pada titik ujung jempol apakah koordinatnya lebih rendah daripada titik dibawahnya (artinya jari membuka)
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # melakukan perulangan untuk mengecek semua titik ujung jari kecuali jempol
        for id in range(1, 5):
            # membandingkan sumbu y pada titik ujung jari apakah koordinatnya lebih rendah daripada 2 titik dibawahnya (artinya jari membuka)
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # mengambil jumlah jari yang terbuka
        totalFingers = fingers.count(1)
        # print(totalFingers)

        # merender foto diatas img/video yang posisinya sesuai dengan lebar dan tinggi foto dan jumlah jari yang terbuka
        h, w, c = overlayList[totalFingers-1].shape
        img[0:h, 0:w] = overlayList[totalFingers-1]

        # merender angka
        cv2.rectangle(img, (20, 255), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)

    # untuk menghitung fps
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    # menambahkan text fps ke img/video
    cv2.putText(img, f'FPS : {int(fps)}', (400, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # merender img/video dan menajalankan kamera
    cv2.imshow("Image", img)
    # untuk memberikan delay 1ms
    cv2.waitKey(1)