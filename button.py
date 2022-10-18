from typing import Tuple
import pygame
class Button():
    def __init__(self, x, y, width, height,color, boder):
        self._color = color
        self._x = x
        self._y = y
        self._height = height
        self._width = width
        self._boder = boder
        self._activate = False

    def draw(self, window):
        pygame.draw.rect(window, self._color, (self._x, self._y, self._width, self._height), self._boder)


    def click(self, x, y):
        if self._x <= x <= self._x + self._width and self._y <= y <= self._y + self._height:
            if self._activate == True :
                self._activate = False
            else : self._activate = True
        else : self._activate = False 

    def not_activate(self):
        self._activate = False

    def is_activate(self):
        return self._activate


class ButtonImage(Button):
    def __init__(self, x, y,height,width):
        self._x = x
        self._y = y
        self._height = height
        self._width = width
        self._activate = False

    def draw(self, window,img):
        window.blit(img,(self._x,self._y))
    
    def get_aim(self, x, y):
        if self._x <= x <= self._x + self._width and self._y <= y <= self._y + self._height:
            return True
        else : return False

    

class InputText_Button(Button):
    def __init__(self, x, y, width, height, color,boder):
        super().__init__(x, y, width, height,color, boder)
        self.__inputtext = ''
        self.__text_val = 0.0
        self._received_val = False

    def draw(self, window):
        super().draw(window)

    def received_val(self):
        self._received_val = True
        
    def set_input(self):
        self.__text_val = float(self.__inputtext)

    def evinput_activate(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.__inputtext = self.__inputtext[:-1]
            else :
                if event.unicode.isnumeric() or event.unicode == '.' :
                    if len(self.__inputtext) <= 3:
                        a = event.unicode
                        if self.__inputtext == '' and a == '.':
                            pass
                        else : 
                            if '.' in self.__inputtext and a == '.' :
                                pass
                            else : self.__inputtext += a
            if event.key == pygame.K_RETURN and self.__inputtext != "":
                self.set_input()

    def update(self,window):
        self.__text_font = pygame.font.Font("font\Font.ttf", 35)
        self.font_surface = self.__text_font.render(self.__inputtext, 1, (0,0,0))   
        window.blit(self.font_surface,((self._x+50),(self._y+20)))

    def get_input_raw(self):
        return self.__inputtext
    def get_input_val(self):
        return self.__text_val