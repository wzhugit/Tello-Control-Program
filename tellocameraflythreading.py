import djitellopy

import cv2

import threading

import time

import numpy as np

import pygame

class MovementThread(threading.Thread):
    def __init__(self,drone):
        threading.Thread.__init__(self)
        self.drone = drone

    def run(self):
        time.sleep(2)
        print(self,drone.get_battery())
        # 起飞
        self.drone.takeoff()
        time.sleep(2)
        #drone.connect()

        # 前进20cm(范围20-500)
        self.drone.move_forward(20)
        time.sleep(2)

        # 后退20cm(范围20-500)
        self.drone.move_back(20)
        time.sleep(2)

        # 左移20cm
        self.drone.move_left(20)
        time.sleep(2)

        # 右移20cm
        self.drone.move_right(20)
        time.sleep(2)

        # 旋转90°
        self.drone.rotate_counter_clockwise(90)
        time.sleep(2)

        
        # 左翻滚
        drone.flip('l')
        time.sleep(2)
        

        #发送RC控制指令
        #send_rc_control(self, left_right_velocity, forward_backward_velocity,
        #up_down_velocity, yaw_velocity) （数值全为整数，范围-100-100）

        self.drone.send_rc_control(3,3,4,2)
        time.sleep(2)

        self.drone.send_rc_control(0,0,0,20)
        time.sleep(2)

        # 降落
        self.drone.land()


class VideoThread(threading.Thread):
    def __init__(self,drone,screen,FPS):
        threading.Thread.__init__(self)
        self.drone = drone
        self.screen = screen
        self.FPS = FPS

    def run(self):
        #self.drone.connect()
        

        '''
        # Creat pygame window
        # 创建pygame窗口
        pygame.display.set_caption("Tello video stream")
        self.screen = pygame.display.set_mode((960,720),flags = pygame.SCALED)
        '''
        
        img = self.drone.get_frame_read().frame
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img = np.rot90(img)
        img = np.flipud(img)
        img = pygame.surfarray.make_surface(img)

        self.screen.blit(img,(0,0))
        pygame.display.update()
        
        #cv2.imshow("drone",img)
    
    
        time.sleep(1/self.FPS)
    
        while True:
            # In reality you want to display frames in a seperate thread. Otherwise
            #  they will freeze while the drone moves.
            # 在实际开发里请在另一个线程中显示摄像头画面，否则画面会在无人机移动时静止
       
            frame_read = self.drone.get_frame_read()
            img = self.drone.get_frame_read().frame
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            img = self.drone.get_frame_read().frame

            #img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            img = np.rot90(img)
            img = np.flipud(img)
            img = pygame.surfarray.make_surface(img)

            self.screen.blit(img,(0,0))
            pygame.display.update()
            time.sleep(1/self.FPS)


def main(drone):
    drone.connect()

    # 打开视频流
    drone.streamon()

    print(drone.get_battery())

    # Creat pygame window
    # 创建pygame窗口
    pygame.display.set_caption("Tello video stream")
    screen = pygame.display.set_mode((960,720),flags = pygame.SCALED)
    
    threads = [MovementThread(drone),VideoThread(drone,screen,120)]

    for thread in threads:
        thread.start()
        #thread.join()
    


if __name__ == '__main__':
    drone = djitellopy.Tello()

    main(drone)

    
