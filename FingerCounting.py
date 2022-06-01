'''
Tugas Besar ASD Kelompok 15
Anggota Kelompok :
- Naufal Hakim (H1A021045)
- Fahrian Azizi (H1A021049)
- M. Saujana Shafi Kehaulani (H1A021053)
- Yohanes Rony Setiawan (H1A021065)
- Ghoni Dzulqurnain (H1A021071)
copyright 2022
'''

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

# sorting list nama foto
myList.sort(key=lambda f: int(f.split('.')[0]))

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

# untuk mengecek posisi jempol
def thumbChecker(noHand):
    # membandingkan nilai x dari titik 1 dan 0 pada tangan
    if lmList[noHand][1][1] > lmList[noHand][0][1]: # (tangan kanan)
            # membandingkan nilai x dari titik 4 dan 3 pada jempol
            if lmList[noHand][tipIds[0]][1] > lmList[noHand][tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
    else: # (tangan kiri)
        # membandingkan nilai x dari titik 4 dan 3 pada jempol
        if lmList[noHand][tipIds[0]][1] < lmList[noHand][tipIds[0]-1][1]: # jari membuka
            fingers.append(1)
        else:
            fingers.append(0)

# untuk mengecek posisi jari
def fingerChecker(noHand):
    # membandingkan nilai y dari titik diujung jari dengan 2 titik dibawahnya
    if lmList[noHand][tipIds[id]][2] < lmList[noHand][tipIds[id]-2][2]: # jari membuka
        fingers.append(1)
    else:
        fingers.append(0)

while True:
    # membuat/membaca frame kamera
    success, img = cap.read()

    # membuat img/video baru yang sudah mendeteksi tangan
    img = detector.findHands(img)

    # mengambil posisi titik pada jari
    lmList = detector.findPosition(img, draw=False)

    # mengecek apakah ada tangan yang terdeteksi
    if len(lmList[0]) != 0:
        # list untuk menampung jari mana saja yang membuka
        fingers = []

        # mengecek jempol pada 1 tangan
        thumbChecker(0)

        # mengecek apakah ada 2 tangan dilayar
        if(len(lmList[1]) != 0):
            thumbChecker(1) # mengecek jempol pada tangan yang satu lagi (membuka/menutup)

        # melakukan perulangan untuk mengecek semua titik ujung jari kecuali jempol
        for id in range(1, 5):
            # mengecek jari pada 1 tangan
            fingerChecker(0)

            # mengecek apakah ada 2 tangan dilayar
            if(len(lmList[1]) != 0):
                fingerChecker(1) # mengecek jari pada tangan yang satu lagi (membuka/menutup)

        # mengambil jumlah jari yang terbuka
        totalFingers = fingers.count(1)

        # merender foto diatas img/video yang posisinya sesuai dengan lebar dan tinggi foto dan jumlah jari yang terbuka
        h, w, c = overlayList[totalFingers-1].shape
        img[0:h, 0:w] = overlayList[totalFingers-1]

        # merender angka
        cv2.rectangle(img, (20, 350), (170, 450), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 430), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 10)

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