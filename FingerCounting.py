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
cap.set(4, hCam)
cap.set(3, wCam)

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
    if lmList[noHand][1][1] > lmList[noHand][0][1]:
        # membandingkan nilai x dari titik 4 dan 3 pada jempol
        if lmList[noHand][tipIds[0]][1] > lmList[noHand][tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
    else:
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
    img_flip = cv2.flip(img,1)

    # membuat img/video baru yang sudah mendeteksi tangan
    img_flip = detector.findHands(img_flip)

    # mengambil posisi titik pada jari
    lmList = detector.findPosition(img_flip, draw=False)

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

        newFingers = ''.join(str(e) for e in fingers)
        if newFingers == '01110':
            totalFingers = 6
        if newFingers == '01101':
            totalFingers = 7
        if newFingers == '01011':
            totalFingers = 8
        if newFingers == '00111':
            totalFingers = 9
        if newFingers == '10000':
            totalFingers = 10
        print(fingers)

        # merender foto diatas img/video yang posisinya sesuai dengan lebar dan tinggi foto dan jumlah jari yang terbuka
        h, w, c = overlayList[totalFingers-1].shape
        img_flip[0:h, 0:w] = overlayList[totalFingers-1]

        # merender angka
        cv2.rectangle(img_flip, (20, 350), (170, 450), (255, 255, 255), cv2.FILLED)
        cv2.putText(img_flip, str(totalFingers), (45, 430), cv2.FONT_HERSHEY_PLAIN, 5, (20, 20, 20), 10)

    # untuk menghitung fps
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    # menambahkan text fps ke img/video
    cv2.putText(img_flip, f'FPS : {int(fps)}', (480, 40),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

    # merender img/video dan menajalankan kamera
    cv2.imshow("Image", img_flip)
    # untuk memberikan delay 1ms
    cv2.waitKey(1)
