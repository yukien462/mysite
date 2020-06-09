
#------------------------
# Nakaitsu write
# 2020 06.08
# This is test sample.
# video/CutResult.text ファイル作成
# 切り取り細長に戻す　閾値パラメータをガウス値に変更
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

    #----  データバー画像きりだし  (バー部分幾分歪みあり)　細長い形
    #img_tmp = imag[673 : 681 , 698 : 1120]
    img_tmp = imag[673 :681 , 702 : 1120]
    #----- 色基準で2値化する。
    gray_image = cv2.cvtColor(img_tmp, cv2.COLOR_BGR2GRAY)
    #===== 適応的閾値処理 ======================================
    # http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html
    # 参考　===================================================
    # save image debug用にフォルダに書き込む
    file_path = os.path.join(bace_path, 'Debug_img')
    os.makedirs(file_path, exist_ok=True)
    cv2.imwrite("Debug_img/gray_"+str(image_file.split('_', 4)[-1]), gray_image)
    # black white (閾値を中満指定の固定値とする)
    ret, bw_image = cv2.threshold(gray_image, 190,255,cv2.THRESH_BINARY)
    # black white （近傍領域の中央値を閾値とする）
    #bw_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    # black white （近傍領域の重み付け平均値を閾値とします。重みの値はGauusian分布になる様に計算してされます）
    #bw_image = cv2.adaptiveThreshold(gray_image, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

    # Otsu's thresholding
    #ret,bw_image = cv2.threshold(gray_image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # save image debug用にフォルダに書き込む
    cv2.imwrite("Debug_img/bw_"+str(image_file.split('_', 4)[-1]), bw_image)

    #---- 画像認識をする 戻り値（オブジェクトの座標を保持している配列、階層構造情報を保持している配列）
    contours, hierarchy = cv2.findContours(bw_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    detect_count = 0
    ret = 0 
    #各輪郭に対する処理　オブジェクト毎に処理
    for i in range(0, len(contours)):
    # 輪郭の領域を計算        
        area = cv2.contourArea(contours[i])

        # ノイズ（小さすぎる領域）と全体の輪郭（大きすぎる領域）を除外
        if area < 1e2 or 1e5 < area:
            continue

        # 外接矩形
        if len(contours[i]) > 0:
            rect = contours[i]
            #外接矩形の左上の位置を(x,y)，横と縦のサイズを(w,h)とすると以下の巻数
            x, y, w, h = cv2.boundingRect(rect)
            cv2.rectangle(img_tmp, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # 外接矩形毎に画像を保存
            cv2.imwrite('Debug_img/'+str(image_file.split('_', 4)[-1]) +'_'+ str(detect_count) + '.jpg', img_tmp[y:y + h, x:x + w])

            detect_count = detect_count + 1
            # 横の長さを入力 @@ 最長を入力してみる
            #if w > ret:
            ret += w
    # 外接矩形された画像を表示
    #cv2.imshow('output', img_tmp)
    #cv2.waitKey(0) """

    # 終了処理
    #cv2.destroyAllWindows()
    #return ret
    return (ret/418)*30

#-------- --------------------　------------------------
def GetImagefile(image_path):

     #------ 実行ファイルのディレクトリ名
    bace_path = os.path.dirname(os.path.abspath(__file__)) 
        
    #---- CSVファイルをひらく
    # if os.path.isfile(os.path.join(bace_path,'ExtractFueleconomy_result')) == True:
    #     print('ExtractFueleconomy_resultファイルが存在します')
    #     sys.exit(0);
    csv_file =  open('ExtractFueleconomy_result','w')
    writer = csv.writer(csv_file)    
   # files = natsorted(os.listdir(image_path))
    files = natsorted(os.listdir(os.path.join(bace_path, image_path)))
    
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
