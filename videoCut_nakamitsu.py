
#------------------------
# Nakaitsu write
# 2020 05.21
# This is test sample.
# ２箇所設定箇所あり
#------------------------
import cv2
import os
import numpy as np



#--------　動画ファイルを　frame 取得する　------------------------ 
def save_all_frames(video_path, dir_path, basename, ext='jpg'):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    n = 0
    frameCount = 0
    #===================================================
    #-   10000 まで　すべてのframe を取得するには while(1):
    #===================================================
    while frameCount < 100000:
        ret, frame = cap.read()
        if ret:
            frameCount += 1

            #-------- 取得する frameCount を設定する
            #====================================
            # imgファイルに記述する　fileCount 設定
            #====================================           
            if frameCount >9000 and frameCount <= 10000:
                cv2.imwrite('{}_{}.{}'.format(base_path, str(frameCount), ext), frame)
                
        else:
            return



save_all_frames('../video_data/cam_panel.avi', 'video/CutResult', 'cam_panel_img')



