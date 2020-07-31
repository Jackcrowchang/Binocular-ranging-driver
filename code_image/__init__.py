import cv2
import time

AUTO = False  # 自动拍照，或手动按s键拍照
INTERVAL = 2 # 自动拍照间隔

cv2.namedWindow("left")
cv2.namedWindow("right")
cv2.moveWindow("left", 0, 0)
cv2.moveWindow("right", 400, 0)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)  # 设置分辨率
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
left_camera = cv2.VideoCapture(0)
right_camera = cv2.VideoCapture(1)


counter = 0
utc = time.time()
pattern = (12, 8) # 棋盘格尺寸
folder = "./snapshot/" # 拍照文件目录


def shot(pos, frame):
    global counter
    path = folder + pos + "_" + str(counter) + ".jpg"

    cv2.imwrite(path, frame)
    print("snapshot saved into: " + path)


while True:
    ret, pic = cap.read()
    left_frame = pic[0:720, 0:1280]
    right_frame = pic[0:720, 1280:2560]
    cv2.imshow("left", left_frame)
    cv2.imshow("right", right_frame)

    now = time.time()
    if AUTO and now - utc >= INTERVAL:
        shot("left", left_frame)
        shot("right", right_frame)
        counter += 1
        utc = now

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    elif key == ord("s"):
        shot("left", left_frame)
        shot("right", right_frame)
        counter += 1

left_camera.release()
right_camera.release()
cv2.destroyWindow("left")
cv2.destroyWindow("right")