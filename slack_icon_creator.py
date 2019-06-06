# coding utf-8
import cv2
import numpy as np
import sys
import os

SLACK_ICON_MAXSIZE = (2000,2000)
SLACK_ICON_MINSIZE = (512,512)

#　画像が存在するかどうか
if len( sys.argv ) != 2:
    print('Error:アイコンにしたい画像ファイルをひとつ指定してください')
    exit()

if not os.path.exists(sys.argv[1]):
    print('Error:そのようなファイルは存在しません')
    exit()

print('整形を開始します')

img = cv2.imread(sys.argv[1])

getSmaller = lambda width, hight: width if width < hight else hight
squareSize = getSmaller(img.shape[0],img.shape[1])
temp_img = np.zeros( (squareSize, squareSize, img.shape[2] ),np.uint8 )

# 画像を正方形に切り取る（長い方の端から切り取っていく）
if img.shape[0] > img.shape[1]:
    left = 0;
    right = img.shape[0]
    while right - left > img.shape[1]:
        left += 1
        if right - left <= img.shape[1]:
            break
        right -= 1
    temp_img = img[left:right,:,:]

elif img.shape[0] < img.shape[1]:
    # こっちは動作確認済み
    upper = 0;
    under = img.shape[1]
    while under - upper > img.shape[0]:
        upper += 1
        if under - upper <= img.shape[0]:
            break
        under -= 1
    temp_img = img[:,upper:under,:]

# slackのアイコンは2000ピクセルより大きいサイズの画像は受け付けないため、
# ここでリサイズする
if temp_img.shape[0] > SLACK_ICON_MAXSIZE[0]:
    temp_img = cv2.resize(temp_img,SLACK_ICON_MAXSIZE)
elif temp_img.shape[0] < SLACK_ICON_MINSIZE[0]:
    temp_img = cv2.resize(temp_img,SLACK_ICON_MINSIZE)

print('整形し終わりました')
print('保存ファイル名を指定してください')
file_name = input()
cv2.imwrite(file_name + ".jpg", temp_img)
