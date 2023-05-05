from socket import socket, AF_INET, SOCK_STREAM

HOST        = 'localhost'
PORT        = 51000

CHR_CAN     = '\18'
CHR_EOT     = '\04'

def com_send(mess):

    while True:
        try:
            # 通信の確立
            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect((HOST, PORT))

            # メッセージ送信
            sock.send(mess.encode('utf-8'))

            # 通信の終了
            sock.close()
            break

        except:
            print ('retry: ' + mess)

def proc():
    com_send('message test')

def exit():
    com_send(CHR_EOT)

def cancel():
    com_send(CHR_CAN)
    
import sys
import os
import pathlib
from time import sleep
from concurrent.futures import ThreadPoolExecutor

import cv2
import numpy as np
import boto3
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import sys

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a11dq6o28la5x0-ats.iot.ap-northeast-1.amazonaws.com"
CLIENT_ID = "testDevice"
PATH_TO_CERT = "setting/8f6c903c31555313ea9c21f6cd301ee4200005b2035c833390bf84a757527214-certificate.pem.crt"
PATH_TO_KEY = "setting/8f6c903c31555313ea9c21f6cd301ee4200005b2035c833390bf84a757527214-private.pem.key"
PATH_TO_ROOT = "setting/AmazonRootCA1.pem"
MESSAGE = "Hello World"
TOPIC = "data/test"

# スケールや色などの設定
scale_factor = .15
green = (0,255,0)
red = (0,0,255)
frame_thickness = 2
camera = cv2.VideoCapture(0)
rekognition = boto3.client('rekognition')

# フォントサイズ
fontscale = 1.0
# フォント色 (B, G, R)
color = (0, 120, 238)
# フォント
fontface = cv2.FONT_HERSHEY_DUPLEX 

import datetime

# Rekognitionの認識結果を配列で保存
#人と犬の位置情報を格納する配列の作成
Dtime = []
max_n = []
per1 = [] 
per11 = []
check1 = []
per2 = [] 
per21 = []
check2 = []
per3 = [] 
per31 = []
check3 = []
per4 = [] 
per41 = []
check4 = []
per5 = []
per51 = []
check5 = []
per61 = []
per6 = []
check6 = []
per71 = []
per7 = []
check7 = []
per81 = []
per8 = []
check8 = []
per_result = []
ti = []
#n = 1
num = 0
status = 0.0
hikensya = input("被験者：")
import time

import matplotlib.pyplot as plt
import numpy as np

# 描画領域を取得
fig, ax = plt.subplots(1, 1)
# y軸方向の描画幅を指定
ax.set_ylim((0, 1))
# x軸:時刻
x = np.arange(0, 30, 0.5)

#fpsを20.0にして撮影したい場合はfps=20.0にします
fps = 5.0
w = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))#カメラの幅を取得
h = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))#カメラの高さを取得

print("start")

setData1 = {}
class PlotGraph:
    def __init__(self):
        self.status = 0
        
        # データを更新する関数を呼び出す時間を設定
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.timeout.connect(self.servo)
        self.timer.start(200)
        self.update()
        
    def update(self):
        end = time.time()
        setdata = self.input_Data()
        
    def servo(self):
        if self.status == 1:
            com_send("1")
            self.status == 0
        elif self.status == 2 or self.status == 5 or self.status == 7:
            com_send("2")
            self.status == 0
        elif self.status == 3 or self.status == 4:
            com_send("3")
            self.status == 0
        elif self.status == 6:
            com_send("4")
            self.status == 0
        elif self.status == 8:
            com_send("5")
            self.status == 0
        else:
            cancel()
            
    def input_Data(self):
        global status
        # フレームをキャプチャ取得
        ret, frame = camera.read()
        height, width, channels = frame.shape[:3]
        
        #cv2.imshow('cap', frame)             # フレームを画面に表示
        # jpgに変換 画像ファイルをインターネットを介してAPIで送信するのでサイズを小さくしておく
        small = cv2.resize(frame, (int(width * scale_factor), int(height * scale_factor)))
        ret, buf = cv2.imencode('.jpg', small)
            
            # Amazon RekognitionにAPIを投げる
        faces = rekognition.detect_faces(Image={'Bytes':buf.tobytes()}, Attributes=['ALL'])
            # 顔の周りに箱を描画する
        for face in faces['FaceDetails']:
            dt_now = datetime.datetime.now()
            smile = face['Smile']['Value']
            cv2.rectangle(frame,
                        (int(face['BoundingBox']['Left']*width),
                        int(face['BoundingBox']['Top']*height)),
                        (int((face['BoundingBox']['Left']+face['BoundingBox']['Width'])*width),
                        int((face['BoundingBox']['Top']+face['BoundingBox']['Height'])*height)),
                        green if smile else red, frame_thickness)
            emothions = face['Emotions']
            i = 0
            for emothion in emothions:
                cv2.putText(frame,
                            str(emothion['Type']) + ": " + str(emothion['Confidence']),                           
                            (25, 40 + (i * 25)),
                            fontface,
                            fontscale,
                            color)
                if str(emothion['Type']) == 'HAPPY':
                    Dtime.append(str(dt_now))
                    ti.append(len(ti) + 1)
                    per1.append(str(emothion['Confidence']))
                    per11.append(emothion['Confidence'])
                    check1.append(emothion['Confidence'])
                elif str(emothion['Type']) == 'CONFUSED':
                    per2.append(str(emothion['Confidence']))
                    per21.append(emothion['Confidence'])
                    check2.append(emothion['Confidence'])
                elif str(emothion['Type']) == 'SURPRISED':
                    per3.append(str(emothion['Confidence']))
                    per31.append(emothion['Confidence'])
                    check3.append(emothion['Confidence'])
                elif str(emothion['Type']) == 'FEAR':
                    per4.append(str(emothion['Confidence']))
                    per41.append(emothion['Confidence'])
                    check4.append(emothion['Confidence'])
                elif str(emothion['Type']) == 'ANGRY':
                    per5.append(str(emothion['Confidence']))
                    per51.append(emothion['Confidence'])
                    check5.append(emothion['Confidence'])
                elif str(emothion['Type']) == 'SAD':
                    per6.append(str(emothion['Confidence']))
                    per61.append(emothion['Confidence'])
                    check6.append(emothion['Confidence'])
                elif str(emothion['Type']) == 'DISGUSTED':
                    per7.append(str(emothion['Confidence'])) 
                    per71.append(emothion['Confidence'])
                    check7.append(emothion['Confidence'])
                elif str(emothion['Type']) == 'CALM':
                    per8.append(str(emothion['Confidence']))
                    per81.append(emothion['Confidence'])
                    check8.append(emothion['Confidence'])
                if len(check1) == 5:
                    c = list(range(8))
                    c[0] = sum(check1)
                    c[1] = sum(check2)
                    c[2] = sum(check3)
                    c[3] = sum(check4)
                    c[4] = sum(check5)
                    c[5] = sum(check6)
                    c[6] = sum(check7)
                    c[7] = sum(check8)
                    if (c.index(max(c))) == 0:
                        self.status = 1
                    elif (c.index(max(c))) == 1:
                        self.status = 2
                    elif (c.index(max(c))) == 2:
                        self.status = 3
                    elif (c.index(max(c))) == 3:
                        self.status = 4
                    elif (c.index(max(c))) == 4:
                        self.status = 5
                    elif (c.index(max(c))) == 5:
                        self.status = 6
                    elif (c.index(max(c))) == 6:
                        self.status = 7
                    elif (c.index(max(c))) == 7:
                        self.status = 8
                    self.servo()
                    self.status = 0
                    check1.clear()
                    check2.clear()
                    check3.clear()
                    check4.clear()
                    check5.clear()
                    check6.clear()
                    check7.clear()
                    check8.clear()
        
        setData1['ti'] = ti[len(ti) - 1]
        setData1['per11'] = per11[len(ti) - 1]
        setData1['per21'] = per21[len(ti) - 1]
        setData1['per31'] = per31[len(ti) - 1]
        setData1['per41'] = per41[len(ti) - 1]
        setData1['per51'] = per51[len(ti) - 1]
        setData1['per61'] = per61[len(ti) - 1]
        setData1['per71'] = per71[len(ti) - 1]
        setData1['per81'] = per81[len(ti) - 1]
        
        return setData1

if __name__ == "__main__":
    
    graphWin = PlotGraph()
    QtGui.QApplication.instance().exec_()
    
    camera.release()
    cv2.destroyAllWindows()