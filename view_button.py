import pygame
import time

class Button():
    def __init__(self, function=None, position:list=[0,0], size:list=[40,10],  text:list=[], color:list=[173,173,173],
                 pressed_color:list=[0,0,0]):
        self.position=position
        self.id=int(time.time()*1000)
        self.color=color
        self.pressed=False
        self.is_toggled=False
        self.pressed_color=pressed_color
        self.delay_time=0.1
        self.text=text
        self.size=size
        self.current_text_id=0
        self.function=function
        self.click_time=0

    def change_text(self):
        self.current_text_id=(self.current_text_id+1)%len(self.text)

    def clicked(self, click):
        pressed= (click[0]>=self.position[0] and click[0]<=self.position[0]+self.size[0]) and (click[1]>=self.position[1] and click[1]<=self.position[1]+self.size[1])
        if pressed:
            self.change_text()
            self.on_pressed()
            if self.function!=None:
                self.function()
        return pressed

    def on_pressed(self):
        self.pressed=True
        self.is_toggled=not self.is_toggled
        self.click_time=time.time()

    def unpress(self):
        if time.time()-self.click_time>=self.delay_time:
            self.pressed=False

    def draw(self, screen):
        self.unpress()
        myfont = pygame.font.SysFont('Arial', 14)
        if self.pressed:
            pygame.draw.rect(screen, self.color, (self.position[0] - 1, self.position[1] - 1,
                                                  self.size[0] + 1, self.size[1] + 1))
            pygame.draw.rect(screen, self.pressed_color, (self.position[0], self.position[1],
                                          self.size[0], self.size[1]))
            textsurface = myfont.render(self.text[self.current_text_id], False, self.color)
        else:
            pygame.draw.rect(screen, self.pressed_color, (self.position[0] + 1, self.position[1] + 1,
                                                  self.size[0] , self.size[1]))
            pygame.draw.rect(screen, self.color, (self.position[0], self.position[1],
                                          self.size[0], self.size[1]))
            textsurface = myfont.render(self.text[self.current_text_id], False, self.pressed_color)
        text_width = textsurface.get_width()
        text_height = textsurface.get_height()
        mid_x=self.position[0]+self.size[0]/2
        mid_y=self.position[1]+self.size[1]/2
        screen.blit(textsurface, [mid_x - text_width / 2, mid_y - text_height / 2])