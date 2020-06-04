
#------------------------
# Nakaitsu write
# 2020 06.04
# This is test sample.
# video/CutResult.text ファイル作成
# 閾値　最適化165 => zero は　0.11あたりの小数値
#------------------------
import cv2
import os
import numpy as np
import csv
import sys
import random
from natsort import natsorted

#-------- 画像からデータを取得する　------------------------
def ExtractValue(image_file):
    #------ 実行ファイルのディレクトリ名
    bace_path = os.path.dirname(os.path.abspath(__file__)) 

    #----  画像読み込み
    imag = cv2.imread(image_file)

    #----  データバー画像きりだし  (バー部分幾分歪みあり)
    #img_tmp = imag[673 : 681 , 698 : 1120]
    img_tmp = imag[673 :681 , 702 : 1120]
    #----- 色基準で2値化する。
    gray_image = cv2.cvtColor(img_tmp, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("gray_image_"+str(image_file.split('_', 4)[-1]), gray_image)
    # black white
    ret, bw_image = cv2.threshold(gray_image, 190,255,cv2.THRESH_BINARY)
    # save image
    cv2.imwrite("black_white_"+str(image_file.split('_', 4)[-1]), bw_image)

    #----- 白色ピクセルをカウントする
    image_size = bw_image.size
    whitePixels = cv2.countNonZero(bw_image)
 
    whiteAreaRatio = (whitePixels/image_size)*100
 
    ## print("White Area [%] : ", whiteAreaRatio)
    ##p rint("ExtractFueleconomy [ km/l ]  : ", whiteAreaRatio*30/100)
    return whiteAreaRatio*30/100

#-------- --------------------　------------------------
def GetImagefile(image_path):

     #------ 実行ファイルのディレクトリ名
    bace_path = os.path.dirname(os.path.abspath(__file__)) 
        
    #---- CSVファイルをひらく
    # if os.path.isfile(os.path.j       oin(bace_path,'ExtractFueleconomy_result')) == True:
    #     print('ExtractFueleconomy_resultファイルが存在します')
    #     sys.exit(0);
    csv_file =  open('ExtractFueleconomy_result','w')
    writer = csv.writer(csv_file)    
    files = natsorted(os.listdir(image_path))
    #print(type(files))
    
    count = 0
    #-----リスト内のファイル名を取得する
    for file in files:
        #----  関数呼び出し
        file_path = os.path.join(bace_path, os.path.join(image_path,file))
        value = ExtractValue(file_path)
        #----  CSVに記述
        tmp_file_name = file.split('.', 1)[0]
        writer.writerow([str(tmp_file_name.split('_', 3)[-1]) ,str(value)])
        count += 1
    #--- CSVファイルを閉じる
    csv_file.close()
    
#GetImagefile('/')  
GetImagefile('video/CutResult_select')
#ExtractValue(image_file)
