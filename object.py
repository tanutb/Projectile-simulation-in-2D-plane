
import pygame
from pygame import surface
from pygame import image
from pygame.event import post
import pygame.math
import math
from pygame.mouse import get_pos
from pygame.transform import scale


class Gobject:
    def __init__(self,h,k):
        self._center_x = h
        self._start_point = h
        self._center_y = k
        self._Start_drawing = False
        self._img_scale = (0,0)
        self._anime_finished = False
        self._time_delay = 0
        self._anime_rotate_angle = 0

    def draw(self,window,a):
            if type(a) == str :
                img = pygame.image.load(a)
                center_img = img.get_rect()
                window.blit(img,(self._center_x-center_img.center[0],self._center_y-center_img.center[1]))
            else : 
                center_img = a.get_rect()
                window.blit(a,(self._center_x-center_img.center[0],self._center_y-center_img.center[1]))

    def anime_appear_draw(self,window,arr):
        if self._Start_drawing == True : 
            scale = pygame.Surface.get_width(arr)
            if self._img_scale[0] != scale:
                a = list(self._img_scale)
                a[0] += 10
                a[1] += 10
                self._img_scale = tuple(a)
            img_tran = pygame.transform.scale(arr,self._img_scale)
            center_img = img_tran.get_rect()
            window.blit(img_tran,(self._center_x-center_img.center[0],self._center_y-center_img.center[1]))
            self._anime_finished = True

    def Start_drawing(self):
        self._Start_drawing = True
    def set_pos_pixel(self,x):
        self._center_x = self._start_point +( x *190)
    def anime_finish(self):
        return self._anime_finished

class GameObject_withProjectile(Gobject):
    g = -9.81
    def __init__(self,h,k,img_ball,img_path):
        super().__init__(h,k)
        self.__center = [h,k]
        self.__img_path = img_path
        self.__img_ball = img_ball
        self.__finish = False
        self.__angle = (45*math.pi/180)
        self.__pos_x = 0
        self.__vel = 0
        self.__init_accel = pygame.Vector2()
        self.__init_vel = pygame.Vector2()
        self.__init_pos = pygame.Vector2()
        self.__vel_in = pygame.Vector2()
        self.__pos = pygame.Vector2()
        self.__time = 0.0
        self.__dt = 0.01
        self.__path = []
        self.__f_path = 0
        self.__img_scale = [pygame.Surface.get_width(self.__img_ball),pygame.Surface.get_height(self.__img_ball)]

    def set_pos_x(self,x):
        self.__pos_x = x
        self.__vel = math.sqrt(self.__pos_x*(-self.g))
        self.__init_accel = pygame.Vector2(0,self.g)
        self.__init_vel = pygame.Vector2(math.cos(self.__angle)*self.__vel,math.sin(self.__angle)*self.__vel)
        self.__init_pos = pygame.Vector2(0,0)
        self.__pos = pygame.Vector2()

    def anime_rotating(self,window):
        if self._Start_drawing == False : self.draw(window,"img\Ball.png")
        elif self._Start_drawing == True  and self.__finish != True:
            self._anime_rotate_angle -= 2
            center_img = self.__img_ball.get_rect()
            window.blit(pygame.transform.rotate(self.__img_ball, self._anime_rotate_angle),(self.__center[0]-center_img.center[0],self.__center[1]-center_img.center[1]))
            self.draw_path(window)
        elif self._Start_drawing == True and self.__finish == True :
            self.anime_disappear_draw(window)
            self.draw_path(window)

    def anime_disappear_draw(self,window):
            a = pygame.transform.rotate(self.__img_ball, self._anime_rotate_angle)
            if self.__img_scale[0] > 0:
                self.__img_scale[0] -= 10
                self.__img_scale[1] -= 10
            img_tran = pygame.transform.scale(a,tuple(self.__img_scale))
            center_img = self.__img_ball.get_rect()
            window.blit(img_tran,(self.__center[0]-center_img.center[0],self.__center[1]-center_img.center[1]))

    def calculating(self):
        if self.__pos.y >= 0:
            self.__pos = self.__init_pos + self.__init_vel * self.__time + self.__init_accel*(self.__time**2)*0.5
            self.__time += self.__dt
        else :
             self.__finish = True
        if self.__pos.x > self.__pos_x :
            self.__time -= self.__dt
            self.__pos.x += self.__pos.y
            self.__pos.y = -0.0001
        self._Start_drawing = True
        self.__vel_in = self.__init_vel + self.__init_accel*(self.__time)
        self.__center = [self._center_x+self.__pos.x*190,self._center_y-self.__pos.y*190]
        if self.__f_path == 4:
            self.__path.append(self.__center)
            self.__f_path = 0
        else : self.__f_path += 1

    def draw_path(self,window) :
        center_img = self.__img_path.get_rect()
        for j in self.__path :
            window.blit(self.__img_path,(j[0]-center_img.center[0],j[1]-center_img.center[1]))

    def check_finished(self):
        return self.__finish

    def get_pos_init(self):
        return self.__pos_x

    def get_pos(self):
         a = float("{:.2f}".format(self.__pos.x))
         if self.__pos.y < 0: 
            b = float("{:.2f}".format(-self.__pos.y))
         else : b = float("{:.2f}".format(self.__pos.y))
         return [a,b] 

    def get_vel(self):
        vel_x = float("{:.2f}".format(self.__vel_in.x)) 
        vel_y = float("{:.2f}".format(self.__vel_in.y))   
        return [vel_x , vel_y]
        
    def get_vel_init(self):
        vel = float("{:.2f}".format(self.__vel)) 
        return vel

    def get_time(self):
        a = float("{:.2f}".format(self.__time))
        return a

    def spring_travel(self):
        x = (((1.33884)+math.sqrt((1.33884**2)+(4*135*(1/2)*0.193007*(self.__vel**2))))/(2*135))
        a = float("{:.3f}".format(x))
        return a
    
    def val_all(self):
        a = self.get_pos()
        b = self.get_vel()
        c = self.get_time()
        d = 0.00
        e = 0.00
        if self.__finish == True :
            d = self.spring_travel()
            e = self.get_vel_init()


        return a , c, b , d , e
