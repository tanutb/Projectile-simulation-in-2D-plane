from math import e
from typing import BinaryIO
from pygame import display, image
from pygame.math import disable_swizzling, enable_swizzling
from button import ButtonImage
from button import InputText_Button
from object import GameObject_withProjectile
from object import Gobject
import time
import pygame
import os.path
from tkinter import *
from tkinter import messagebox
import sys

class ui:
    black = (0,0,0)

    img_ball = pygame.image.load("img\Ball.png")   
    img_path = pygame.image.load("img\Path.png")   
    img_start_button = pygame.image.load("img\Start_button.jpg") 
    img_start_button_onaim = pygame.image.load("img\Start_button_onaim.jpg") 
    img_stop_button = pygame.image.load("img\Stop_button.jpg") 
    img_stop_button_onaim = pygame.image.load("img\Stop_button_onaim.jpg")     
    img_save_button = pygame.image.load("img\Save_button.jpg")  
    img_save_button_onaim = pygame.image.load("img\Save_button_onaim.jpg")  
    img_save_button_notac = pygame.image.load("img\Save_button_notac.jpg")  
    img_reset_button = pygame.image.load("img\Reset_button.jpg")  
    img_reset_button_onaim = pygame.image.load("img\Reset_button_onaim.jpg")  
    img_target1 = pygame.image.load("img\Target1_5.png") 
    img_target2_arr = ["img\Town1_1.png","img\Town1_2.png" ,"img\Town1_3.png" ,"img\Town1_4.png" ,"img\Town1_5.png" ,"img\Town1_6.png" ]

    def __init__(self):
      
        self.text_font = pygame.font.Font("font\Font.ttf", 27)
        self.button_save = ButtonImage(80,565,60,170) 
        self.button_start = ButtonImage(1000,475,60,170) 
        self.button_reset = ButtonImage(1000,565,60,170) 
        self.textinput1 = InputText_Button(785,555,185,75,(255,255,255),2)   
        self.target1 = Gobject(130,470)  
        self.target2 = Gobject(130,470)
        self.current_target2_anime = 0
        self.ball1 = GameObject_withProjectile(130,470,self.img_ball,self.img_path)
        self.des_text = (1000,75)
        self.userinput1 = ''
        self.__mx = 0
        self.__my = 0
        self.__running = True
        self.__delay = 0
        self.__delay_2 = 0

    def draw_event(self,window):

        if self.button_start.get_aim(self.__mx,self.__my):
            img_start = self.img_start_button_onaim
            if self.button_start.is_activate():
                img_start = self.img_stop_button
                if self.button_start.get_aim(self.__mx,self.__my):
                    img_start = self.img_stop_button_onaim
                else : img_start = self.img_stop_button
        else : 
                if self.button_start.is_activate():
                    img_start = self.img_stop_button
                else : img_start = self.img_start_button
        self.button_start.draw(window,img_start)

        if self.button_reset.get_aim(self.__mx,self.__my):
            img_re = self.img_reset_button_onaim
        else : img_re = self.img_reset_button
        self.button_reset.draw(window,img_re)  

        if self.ball1.check_finished() :
            if self.button_save.get_aim(self.__mx,self.__my):
                img_save = self.img_save_button_onaim
            else : img_save = self.img_save_button
        else : img_save = self.img_save_button_notac
        self.textinput1.draw(window)
        self.button_save.draw(window,img_save)
        self.set_text_display(window)
        self.target1.anime_appear_draw(window,self.img_target1)
        a = pygame.image.load(self.img_target2_arr[self.current_target2_anime])
        self.target2.anime_appear_draw(window,a)
        self.ball1.anime_rotating(window)
        

    def set_text_display(self,window):
        [x,y],time,[velx,vely],s_travel,Vs = self.ball1.val_all()
        pos = self.text_font.render("(x,y): "+ "(" +str(x) + "," +str(y)+")" +" m.",True,(0,0,0))
        time = self.text_font.render("time: "+ str(time) + ' s',True,(0,0,0))
        velx = self.text_font.render("Vel_x: "+ str(velx) +' m/s',True,(0,0,0))
        vely = self.text_font.render("Vel_y: "+str(vely) + ' m/s',True,(0,0,0))
        v_start = self.text_font.render("Vel start: " +str(Vs) + ' m/s',True,(0,0,0))
        s_travel = self.text_font.render("D. spring : "+ str(s_travel) + ' m',True,(0,0,0))
        display = self.text_font.render("Display : ",True,(0,0,0))
        k = self.text_font.render("Spring constant ",True,(0,0,0))
        k2 = self.text_font.render(": 270 N/m",True,(0,0,0))
        l = [k,k2,display,pos,time,v_start,velx,vely,s_travel]
        for i,j in enumerate(l,1) :
            window.blit(j,(self.des_text[0],self.des_text[1]+i*35))
        
    def pos_mouse(self):
        self.button_save.get_aim(self.__mx,self.__my)
        self.button_start.get_aim(self.__mx,self.__my)
        self.button_reset.get_aim(self.__mx,self.__my)
        
    def event_handle(self,window):
        for event in pygame.event.get():
            self.__mx,self.__my = pygame.mouse.get_pos()

            self.pos_mouse()
            if event.type == pygame.QUIT:
                self.__running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.button_reset.click(self.__mx,self.__my)
                if self.textinput1._received_val == False :
                    self.textinput1.click(self.__mx,self.__my)
                if self.ball1.check_finished():
                    self.button_save.click(self.__mx,self.__my)
                if self.textinput1.get_input_val() >= 2 and self.textinput1.get_input_val() <= 4:
                    self.button_start.click(self.__mx,self.__my)
            self.textinput1._activate and self.textinput1.evinput_activate(event)

        if self.textinput1._activate and self.textinput1.get_input_raw() != "":
            self.textinput1.set_input()
            self.ball1.set_pos_x(self.textinput1.get_input_val())

        self.target1.set_pos_pixel(self.ball1.get_pos_init())
        self.target2.set_pos_pixel(self.ball1.get_pos_init())
        if self.button_start.is_activate() :
                self.textinput1.received_val()
                if self.ball1.get_pos_init() >= 3.4 :
                    self.target1.set_pos_pixel(self.ball1.get_pos_init())
                    self.target1.Start_drawing()
                    if self.__delay == 15 :
                        self.target1.anime_finish() and self.ball1.calculating()
                    else : self.__delay += 1
                else : 
                    self.target2.set_pos_pixel(self.ball1.get_pos_init())
                    self.target2.Start_drawing()
                    if self.__delay == 15 :
                        self.target2.anime_finish() and self.ball1.calculating()
                    else : self.__delay += 1
                    
                if self.ball1.check_finished():
                    if self.current_target2_anime == len(self.img_target2_arr)-1 :
                        self.button_start.not_activate()
                    else : 
                        if self.__delay_2 == 2   :
                            self.current_target2_anime += 1
                            self.__delay_2 = 0
                        else : self.__delay_2 += 1
                        
        if self.button_reset.is_activate() :
              self.__init__()  
              self.button_reset.not_activate()


        if self.button_save.is_activate() :
            self.save()
            self.button_save.not_activate()

        self.textinput1.update(window)  
        
    def isrunning(self):
        return self.__running

    def save(self):
            seconds = time.time()
            local_time = time.ctime(seconds)
            if os.path.isfile('SaveLog.txt'):
                file = open("SaveLog.txt","a+")
            else : file = open("SaveLog.txt","w+")
            file.write("==== Save at time  :" + local_time +" ====" + "\n"
                        "Spring constant : 270  N/m."+ "\n"
                        "Input Sx = " + self.textinput1.get_input_raw() + "  m.\n"
                        "Displacement of Spring = " + str(self.ball1.spring_travel()) +"  m.\n")
            Tk().wm_withdraw()
            messagebox.showinfo('Save Alert','Log have been saved successfully')
            file.close()
