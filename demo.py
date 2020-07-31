import cv2
import numpy as np

def resizeImage(image, width=None, height=None, inter=cv2.INTER_AREA):
    newsize = (width, height)
    # 获取图像尺寸
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    # 高度算缩放比例
    if width is None:
        n = height / float(h)
        newsize = (int(n * w), height)
    else:
        n = width / float(w)
        newsize = (width, int(h * n))

    # 缩放图像
    newimage = cv2.resize(image, newsize, interpolation=inter)
    return newimage


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC,1196444237)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)  # 设置分辨率
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while(True):
    # 逐帧捕获
    ret, pic = cap.read()

    # 对各帧的操作
    frame1 = pic[0:720 ,0:1280]
    frame2 = pic[0:720 ,1280:2560]

    # 显示处理结果的帧
    cv2.imshow('frame',frame1)
    cv2.imshow('frame2',frame2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()