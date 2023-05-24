#本程序可在使用手柄控制的同时，显示画面
#pygame joystick test
import djitellopy
import pygame
import cv2
import time
import threading
import numpy as np

def videoshow(drone,screen):
    frame = drone.get_frame_read().frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = np.flipud(frame)
    frame = pygame.surfarray.make_surface(frame)

    screen.blit(frame,(0,0))
    pygame.display.update()
    #time.sleep(1/30)

    while True:
        frame = drone.get_frame_read().frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = np.flipud(frame)
        frame = pygame.surfarray.make_surface(frame)

        screen.blit(frame,(0,0))
        pygame.display.update()
        time.sleep(1/FPS)
        
        #pygame.time.wait(10)   #pygame.time.wait(milliseconds)'''

def main(drone,axenum,FPS):
    done = False
    
    print("Number of axes: {}".format(axenum))

    SPEED = 100
    
    while not done:
        res = [0,0,0,0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.JOYBUTTONDOWN:
                if joystickobj.get_button(0):      #A键
                    drone.takeoff()
                    print('takeoff')

                if joystickobj.get_button(1):      #B键
                    drone.land()
                    print('land')

            

            if event.type == pygame.JOYAXISMOTION:
                for i in range(axenum):                 #左右摇杆,原range(4)
                    axis = joystickobj.get_axis(i)
                    
                    
                    if abs(axis) > 0.3:                     #if abs(axis) > 0.5:
                        if i == 0 or i == 1:                 #左摇杆
                            axis = joystickobj.get_axis(i)   #axis = joystickobj.get_axis(i)
                            res[i] = int(axis * SPEED)        #方向及速度res[i] = int(axis * 50)

                        if i == 2 or i == 3:                 #右摇杆
                            axis = joystickobj.get_axis(i)
                            res[2] = int(axis * SPEED)        #方向及速度res[2] = int(axis * 50)

                        if i == 4:                         #左扳机
                            axis = joystickobj.get_axis(i)
                            res[3] -= int((axis + 1)/2 * SPEED)        #方向及速度res[3] = int(axis * 50)

                        if i == 5:                         #右扳机
                            axis = joystickobj.get_axis(i)
                            res[3] += int((axis + 1)/2 * SPEED)        #方向及速度res[3] = int(-axis * 50)

                drone.send_rc_control(res[0],-res[1],res[3],res[2])    #send_rc_control(self, left_right_velocity, forward_backward_velocity,
#up_down_velocity, yaw_velocity) （数值全为整数，范围-100-100，单位cm/s）
                    
                

            if res == [0,0,0,0]:
                continue

        
        
        pygame.time.wait(int(1000/FPS))    #原为pygame.time.wait(100)，单位毫秒，不能使用time.sleep()，它会阻塞pygame事件loop
                    

##        for i in range(axes):
##            axis = joystickobj.get_axis(i)
##            print("Axis {} value: {:>6.3f}".format(i, axis))
    pygame.quit()
   

            

                


if __name__ == "__main__":
    # Creat pygame window
    # 创建pygame窗口
    pygame.display.set_caption("Tello video stream")
    screen = pygame.display.set_mode((960,720),flags = pygame.SCALED)

    drone = djitellopy.Tello()
    drone.connect()

    print(drone.get_battery())

    # 打开视频流
    drone.streamon()

    FPS = 120

    pygame.init()
    joystickobj = pygame.joystick.Joystick(0)
    joystickobj.init()
    print(joystickobj.get_guid())
    print(joystickobj.get_name())

    axenum = joystickobj.get_numaxes()
        
    videoer = threading.Thread(target = videoshow,args = (drone,screen))
    videoer.start()

    main(drone,axenum,FPS)

    

    #videoer.join()
    
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()
