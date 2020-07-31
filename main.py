import numpy as np
import cv2
import camera_configs
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)  # 设置分辨率
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
threeD = 0
root = tk.Tk()
root.title("双目定位程序")
root.geometry('400x380')
root.config(cursor="arrow")
var = tk.StringVar()
label_x = 0
label_y = 0
label_arg = np.zeros((1, 3))
x_value = 0
y_value = 0
z_value = 0
# debug代码
#label_arg = np.random.rand(19, 3)


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


def Creat_bottom():
    global var
    var.set('等待输入')
    b1 = tk.Button(root, text = '显示双目摄像头原始图像', width = 20,height = 3 , command = Show_camera_capture)
    b1.place(x=140, y=10)
    b2 = tk.Button(root, text = '显示尺度修正的对比图像', width = 20,height = 3 , command = Image_correction)
    b2.place(x=140, y=80)
    b3 = tk.Button(root, text='显示深度图', width=20, height=3, command=Opencv_dispose)
    b3.place(x=140, y=150)
    b4 = tk.Button(root, text='显示空间定位图', width=20, height=3, command=The3d_show)
    b4.place(x=140, y=220)
    b5 = tk.Button(root, text='清空数组', width=7, height=7, command=delete_numpy)
    b5.place(x=70, y=80)
    b6 = tk.Button(root, text='写入数据', width=7, height=7, command=write_numpy)
    b6.place(x=300, y=80)
    l = tk.Label(root,textvariable=var,bg='green', font=('Arial', 12),width=30, height=2)
    l.place(x=80, y=300)


def on_closing():
    if messagebox.askokcancel("Quit", "你想关闭窗口吗?"):
        root.destroy()


def Creat_menu():
    Menubar = tk.Menu(root)
    Filemenu = tk.Menu(Menubar, tearoff = 0)
    Menubar.add_cascade(label='文件', menu=Filemenu)
    Helpmenu = tk.Menu(Menubar, tearoff=0)
    Menubar.add_cascade(label='帮助', menu=Helpmenu)
    Filemenu.add_cascade(label='退出',command = on_closing)
    Helpmenu.add_cascade(label='关于',command = Creat_about)
    root.config(menu=Menubar)


def Creat_about():
    top1=tk.Toplevel()
    top1.title('关于本程序')
    top1.geometry('300x200')
    image = Image.open('code_image\\111.jpg')
    img = ImageTk.PhotoImage(image)
    word_box = tk.Label(top1, text='双目测距软件\r版本：1.0c\rDesigned by Jackcrow\r简介：这是一个简单的双目测距软件')
    canvas1 = tk.Canvas(top1, width = 80 ,height = 80, bg = 'white')
    canvas1.create_image(0, 0, image = img,anchor="nw")
    canvas1.create_image(image.width,0,image = img,anchor="nw")
    canvas1.pack()
    word_box.pack()
    top1.mainloop()


def callbackFunc(e, x, y, f, p):
    global var, threeD
    global label_x, label_y
    global x_value, y_value, z_value
    global label_arg
    label_x = x
    label_y = y
    if e == cv2.EVENT_LBUTTONDOWN:
        print(x)
        str_threeD = str(threeD[y][x][2]/1000)
        if threeD[y][x][2] > 0:
            var.set('所测的距离为：'+str_threeD+'m')
            x_value = abs(x-720)/147
            y_value = abs(y-360)/147
            threeD_array = np.array([x_value, y_value, z_value])
            label_arg = np.insert(label_arg, 1, values = threeD_array, axis=0)
        else:
            var.set('您点击了非法区域')
        l = tk.Label(root, textvariable=var, bg='green', font=('Arial', 12), width=30, height=2)
        l.place(x=80, y=290)
cv2.setMouseCallback("depth", callbackFunc, None)


def Show_camera_capture():
    while True:
        ret, pic = cap.read()
        if not ret:
            var.set('摄像头读取失败')
            break
        frame1 = pic[0:720, 0:1280]
        frame2 = pic[0:720, 1280:2560]
        cv2.namedWindow("Left_camera")
        cv2.namedWindow("Right_camera")
        cv2.imshow("Left_camera", frame1)
        cv2.imshow("Right_camera", frame2)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    cv2.destroyAllWindows()


def Opencv_dispose():
    global threeD
    global label_arg
    global threeD_array
    global x_value, y_value, z_value
    while True:
        ret, pic = cap.read()
        if not ret:
            var.set('摄像头读取失败')
            break
        frame1 = pic[0:720 ,0:1280]
        frame2 = pic[0:720 ,1280:2560]
        img1_rectified = cv2.remap(frame1, camera_configs.left_map1, camera_configs.left_map2, cv2.INTER_LINEAR)
        img2_rectified = cv2.remap(frame2, camera_configs.right_map1, camera_configs.right_map2, cv2.INTER_LINEAR)
        imgL = cv2.cvtColor(img1_rectified, cv2.COLOR_BGR2GRAY)
        imgR = cv2.cvtColor(img2_rectified, cv2.COLOR_BGR2GRAY)
        num = 0
        blockSize = 50
        if blockSize % 2 == 0:
            blockSize += 1
        if blockSize < 5:
            blockSize = 5
        stereo = cv2.StereoBM_create(numDisparities=16 * num, blockSize=blockSize)
        disparity = stereo.compute(imgL, imgR)

        disp = cv2.normalize(disparity, disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        threeD = cv2.reprojectImageTo3D(disparity.astype(np.float32) / 16., camera_configs.Q)
        new_left_image = resizeImage(img1_rectified, 256, 144)
        new_left_image = cv2.cvtColor(new_left_image, cv2.COLOR_BGR2GRAY)
        disp[0:144, 0:256] = new_left_image
        clache = cv2.createCLAHE(clipLimit=2, tileGridSize=(8, 8))
        disp = clache.apply(disp)
        str_threeD0 = str(round(threeD[label_y][label_x][2] / 1000, 5))
        str_threeD1 = str(round(threeD[label_y][label_x][2] / 1000, 4))
        z_value = round(threeD[label_y][label_x][2] / 1000, 3)
        x_value = round(label_x / 1000, 3)
        y_value = round(label_y / 1000, 3)

        font = cv2.FONT_ITALIC
        if threeD[label_y][label_x][2] > 0:
            var.set('所测的距离为：'+str_threeD1+'m')
            cv2.putText(disp, str_threeD0+'m', (10, 500), font, 4, (255, 255, 255), 2, cv2.LINE_AA)
        else:
            var.set('您点击了非法区域')
            cv2.putText(disp, 'Noon', (10, 500), font, 4, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.namedWindow("depth")
        cv2.setMouseCallback("depth", callbackFunc, None)
        cv2.imshow("depth", disp)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        elif key == ord("s"):
            cv2.imwrite("./snapshot/BM_left.jpg", imgL)
            cv2.imwrite("./snapshot/BM_right.jpg", imgR)
            cv2.imwrite("./snapshot/BM_depth.jpg", disp)
    cv2.destroyAllWindows()


def The3d_show():
    global label_arg
    fig = plt.figure()
    ax = Axes3D(fig)

    # X,Y value

    x1 = label_arg[:, 0]  # [ 0  3  6  9 12 15 18 21]
    y1 = label_arg[:, 1]  # [ 1  4  7 10 13 16 19 22]
    z1 = label_arg[:, 2]  # [ 2  5  8 11 14 17 20 23]

    ax.scatter(x1, y1, z1, c='r')

    plt.show()


def delete_numpy():
    global label_arg
    label_arg = np.ones((1, 3))
    var.set('清空数据成功')


def write_numpy():
    global label_arg
    np.savetxt("H:/坚果云/程序/毕设/1.txt", label_arg, fmt='%f', delimiter=',')
    var.set('写入txt成功')


def Image_correction():
    while True:
        ret, pic = cap.read()
        if not ret:
            var.set('摄像头读取失败')
            break
        frame1 = pic[0:240, 0:320]
        frame2 = pic[0:240, 320:640]

        img1_rectified = cv2.remap(frame1, camera_configs.left_map1, camera_configs.left_map2, cv2.INTER_LINEAR)
        img2_rectified = cv2.remap(frame2, camera_configs.right_map1, camera_configs.right_map2, cv2.INTER_LINEAR)
        cv2.namedWindow("Left_camera_origin")
        cv2.namedWindow("Right_camera_origin")
        cv2.namedWindow("Left_camera_correction")
        cv2.namedWindow("Right_camera_correction")
        cv2.moveWindow("Left_camera_origin", 100, 0)
        cv2.moveWindow( "Right_camera_origin", 420, 0)
        cv2.moveWindow("Left_camera_correction", 100, 250)
        cv2.moveWindow("Right_camera_correction", 420, 250)
        cv2.imshow("Left_camera_origin", frame1)
        cv2.imshow("Right_camera_origin", frame2)
        cv2.resizeWindow("Left_camera_correction", 320, 240)
        cv2.imshow("Left_camera_correction", img1_rectified)
        cv2.resizeWindow("Right_camera_correction", 320, 240)
        cv2.imshow("Right_camera_correction", img2_rectified)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    cv2.destroyAllWindows()


Creat_menu()
Creat_bottom()
root.mainloop()