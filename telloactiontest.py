from djitellopy import Tello

import cv2

drone = Tello()

drone.connect()

print(drone.get_battery())

# 起飞
drone.takeoff()

# 前进20cm(范围20-500)
drone.move_forward(20)

# 后退20cm(范围20-500)
drone.move_back(20)

# 左移20cm
drone.move_left(20)

# 右移20cm
drone.move_right(20)

#获取

# 旋转90°
drone.rotate_counter_clockwise(90)

# 左翻滚
drone.flip('l')

#发送RC控制指令
#send_rc_control(self, left_right_velocity, forward_backward_velocity,
#up_down_velocity, yaw_velocity) （数值全为整数，范围-100-100）

drone.send_rc_control(3,3,4,2)

drone.send_rc_control(0,0,0,20)

# 打开视频流
drone.streamon()

frame_read = drone.get_frame_read()

while True:
    # In reality you want to display frames in a seperate thread. Otherwise
    #  they will freeze while the drone moves.
    # 在实际开发里请在另一个线程中显示摄像头画面，否则画面会在无人机移动时静止
   
    img = frame_read.frame
    cv2.imshow("drone",img)

    key = cv2.waitKey(1) & 0xff
    if key == 27: # ESC
        break
    elif key == ord('w'):
        tello.move_forward(30)
    elif key == ord('s'):
        tello.move_back(30)
    elif key == ord('a'):
        tello.move_left(30)
    elif key == ord('d'):
        tello.move_right(30)
    elif key == ord('e'):
        tello.rotate_clockwise(30)
    elif key == ord('q'):
        tello.rotate_counter_clockwise(30)
    elif key == ord('r'):
        tello.move_up(30)
    elif key == ord('f'):
        tello.move_down(30)

# 降落
drone.land()
