#! -*- coding: UTF-8 -*-
import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt
import sys

# 设置寻找亚像素角点的参数，采用的停止准则是最大循环次数30和最大误差容限0.001
criteria = (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.001)

# 获取标定板角点的位置
objp = np.zeros((7 * 9, 3), np.float32)    #9行7列
length = 20 #黑白格长度,单位mm,仅用于计算平移向量
objp[:, :2] = np.mgrid[0:9*length:length, 0:7*length:length].T.reshape(-1, 2)  # 将世界坐标系建在标定板上，所有点的Z坐标全部为0，所以只需要赋值x和y

obj_points = []  # 存储3D点
img_points = []  # 存储2D点

#images = glob.glob("F:\\camdis\\*.png")
images = glob.glob("E:\\image_get_from_TelloDrone\\tellotakepicture*.jpg")
i=0;

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    size = gray.shape[::-1]
    ret, corners = cv2.findChessboardCorners(gray, (9, 7), None)
    #print(ret)

    if ret:

        obj_points.append(objp)

        corners2 = cv2.cornerSubPix(gray, corners, (6, 6), (-1, -1), criteria)  # 在原角点的基础上寻找亚像素角点
        #print(corners2)
        if [corners2]:
            img_points.append(corners2)
        else:
            img_points.append(corners)

        cv2.drawChessboardCorners(img, (9, 7), corners, ret)  # 记住，OpenCV的绘制函数一般无返回值
        i+=1;
        cv2.imwrite('conimg'+str(i)+'.jpg', img)
        
        cv2.imshow('result',img)
        
        cv2.waitKey(1500)
        
    


    print(len(img_points))
    cv2.destroyAllWindows()

    # 标定
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

stdout = sys.stdout

f= open('E:\\image_get_from_TelloDrone\\tellocameraparam.txt','w')

sys.stdout = f

print("ret:", ret)
print(u"内参数矩阵mtx:\n", mtx) # 内参数矩阵
print(u"畸变系数dist:\n", dist)  # 畸变系数   distortion cofficients = (k_1,k_2,p_1,p_2,k_3)
print(u"旋转向量rvecs:\n", rvecs)  # 旋转向量  # 外参数
print(u"平移向量tvecs:\n", tvecs ) # 平移向量  # 外参数

print("-----------------------------------------------------")

img = cv2.imread(images[2])
h, w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))#显示更大范围的图片（正常重映射之后会删掉一部分图像）
print (newcameramtx)
print("------------------使用undistort函数-------------------")
dst = cv2.undistort(img,mtx,dist,None,newcameramtx)
x,y,w,h = roi
dst1 = dst[y:y+h,x:x+w]
cv2.imwrite('calibresult3.jpg', dst1)
print (u"方法一:dst的大小为:", dst1.shape)


f.close()
sys.stdout = stdout


