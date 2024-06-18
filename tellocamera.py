from djitellopy import Tello

import cv2

import time

import numpy as np

drone = Tello()

drone.connect()

print(drone.get_battery())



# 打开视频流
drone.streamon()

time.sleep(1)



while True:
    # In reality you want to display frames in a seperate thread. Otherwise
    #  they will freeze while the drone moves.
    # 在实际开发里请在另一个线程中显示摄像头画面，否则画面会在无人机移动时静止
    frame_read = drone.get_frame_read()
    imgorigin = frame_read.frame
    cv2.imshow("drone",imgorigin)


    
    #imgorigin = cv2.imread('E:\\imgtohough.jpg',cv2.IMREAD_COLOR)

    img = cv2.cvtColor(imgorigin,cv2.COLOR_RGB2BGR)

    cv2.imshow('road',img)


    imggray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #median filter 11x11
    imblurred = cv2.medianBlur(imggray,11)

    cv2.imshow('rodagray',imggray)
    equ = cv2.equalizeHist(imblurred)
    res = np.hstack((imblurred,equ))
    cv2.imwrite('res.png',res)

    edges = cv2.Canny(equ,65,80)

    cv2.imshow('roadedgess',edges)


    lines = cv2.HoughLines(edges, 1, np.pi/180, 80)
    #cv2.HoughLines(edges, 1, np.pi/180, 280) 

    #cv.HoughLines(	image, rho_accuracy, theta_accuracy, threshold
    #[, lines[, srn[, stn[, min_theta[, max_theta]]]]]	) -> 	lines

    '''

    image	8-bit, single-channel binary source image.
            The image may be modified by the function.
            
    lines	Output vector of lines. Each line is represented by a 2 or 3 element
            vector (ρ,θ) or (ρ,θ,votes), where ρ is the distance from the
            coordinate origin (0,0) (top-left corner of the image), θ is the line
            rotation angle in radians ( 0∼vertical line,π/2∼horizontal line ), and
            votes is the value of accumulator.

    rho	Distance resolution of the accumulator in pixels.

    theta	Angle resolution of the accumulator in radians.

    threshold   Accumulator threshold parameter. Only those lines are returned

                that get enough votes ( >threshold ).
                
    srn	For the multi-scale Hough transform, it is a divisor for the distance

            resolution rho. The coarse accumulator distance resolution is rho and

            the accurate accumulator resolution is rho/srn. If both srn=0 and stn=0,

            the classical Hough transform is used. Otherwise, both these parameters

            should be positive.

    stn	For the multi-scale Hough transform, it is a divisor for the distance

            resolution theta.
            
    min_theta	For standard and multi-scale Hough transform, minimum angle

                    to check for lines. Must fall between 0 and max_theta.
                    
    max_theta	For standard and multi-scale Hough transform, an upper bound

                    for the angle. Must fall between min_theta and CV_PI. The

                    actual maximum angle in the accumulator may be slightly less

                    than max_theta, depending on the parameters min_theta and theta. 


    '''


    for line in lines:
        arr = np.array(line[0], dtype=np.float64)
        rho, theta = arr
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = rho * a
        y0 = rho * b
        x1 = int(x0 + 1000 * (-b))                  #这里的100是为了求延长线，其他数值也可以
        y1 = int(y0 + 1000 * a)
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * a)
        # 画线
        cv2.line(imgorigin, (x1, y1), (x2, y2), (0, 0, 255), 2)



    cv2.imshow('houghlines',imgorigin)


    
        
    cv2.waitKey(1)

        


