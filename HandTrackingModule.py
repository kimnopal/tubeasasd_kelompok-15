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
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        # untuk inisialisasi parameter class Hands
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # untuk mendeteksi tangan dengan menginstansiasi class Hands
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity, self.detectionCon, self.trackCon)

        # berisi utility untuk menggambar titik dan garis pada tangan
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        # membuat rgb image untuk dikirimkan ke object hands
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # untuk memproses hasil frame image rgb
        self.results = self.hands.process(imgRGB)

        # mengecek apakah ada tangan yang terdeteksi
        if self.results.multi_hand_landmarks:
            # mengambil setiap tangan yang terdeteksi
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    # menambahkan titik dan garis pada tangan
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, draw=True):
        # menyimpan koordinat semua titik pada kedua tangan
        lmList = [[], []]

        # mengecek apakah ada tangan yang terdeteksi
        if self.results.multi_hand_landmarks:
            # mengambil salah satu tangan sesuai dengan nomor tangan
            myHand = self.results.multi_hand_landmarks

            # mengambil koordinaat masing masing tangan
            for hand in myHand:
                # mengambil informasi dari titik di setiap tangan (berupa nomor id dan koordinat xyz)
                for id, lm in enumerate(hand.landmark):
                    # mengambil lebar dan tinggi dari image untuk dikalikan dengan koordinat agar mendapatkan posisi satuan pixel
                    h, w, c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)

                    # memasukkan koordinat tiap titik pada tangan ke list
                    if(myHand.index(hand) == 0):
                        lmList[0].append([id, cx, cy])
                    else:
                        lmList[1].append([id, cx, cy])


                    # mengecek apakah perlu di gambar
                    if draw:
                        # menggambar lingkaran disetiap titik
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        
        return lmList