# filename: camera_configs.py
import cv2
import numpy as np

left_camera_matrix = np.array([[1083.01172,0., 648.24439],[ 0.,1081.17009, 525.99593],
                               [0., 0., 1.]])
left_distortion = np.array([[-0.47667, 0.22895 ,  -0.00329,   0.00516]])



right_camera_matrix = np.array([[1084.27913,0.,635.77293],
                                [0., 1081.61580, 485.65839],
                                [0., 0., 1.]])
right_distortion = np.array([[ -0.44373, 0.14292,  0.00006,  -0.00151 ,0.00000 ]])

om = np.array([ -0.01413 , -0.00272, 0.00141 ]) # 旋转关系向量
R = cv2.Rodrigues(om)[0]  # 使用Rodrigues变换将om变换为R
T = np.array([ -120.81005,  0.30384, 2.26989 ]) # 平移关系向量

size = (1280, 720) # 图像尺寸

# 进行立体更正
R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(left_camera_matrix, left_distortion,
                                                                  right_camera_matrix, right_distortion, size, R,
                                                                  T)
# 计算更正map
left_map1, left_map2 = cv2.initUndistortRectifyMap(left_camera_matrix, left_distortion, R1, P1, size, cv2.CV_16SC2)
right_map1, right_map2 = cv2.initUndistortRectifyMap(right_camera_matrix, right_distortion, R2, P2, size, cv2.CV_16SC2)