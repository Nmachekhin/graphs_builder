import pygame
from int_input_box import *
from view_button import *
import ctypes

class Parameters_window():
    def __init__(self, wid, hei, screen, end_function, tops_params, links_params):
        self.screen_wid=wid
        self.screen_hei=hei
        self.screen = screen
        self.end_function=end_function
        self.tops_params=tops_params
        self.links_params=links_params
        self.buttons={}
        self.color_inputs={}
        self.radius_inputs={}
        self.set_buttons()
        self.set_inputs()


    def set_buttons(self):
        self.buttons["cancel_btn"]=Button(self.cancel_btn, [10,10], [70,20], ["Скасувати"])
        self.buttons["set_btn"]=Button(self.set_btn, [90,10], [70,20], ["Установити"])

    def cancel_btn(self):
        self.set_inputs()
        self.end_function(False)

    def set_btn(self):
        #колір вершин
        self.tops_params[0][0]=self.color_inputs["tops_body_red"].get_int()
        self.tops_params[0][1]=self.color_inputs["tops_body_green"].get_int()
        self.tops_params[0][2]=self.color_inputs["tops_body_blue"].get_int()
        #колір зв'язків
        self.links_params[0][0]=self.color_inputs["links_red"].get_int()
        self.links_params[0][1]=self.color_inputs["links_green"].get_int()
        self.links_params[0][2]=self.color_inputs["links_blue"].get_int()
        #колір границь вершин/тексту
        self.tops_params[1][0]=self.color_inputs["tops_border_red"].get_int()
        self.tops_params[1][1]=self.color_inputs["tops_border_green"].get_int()
        self.tops_params[1][2]=self.color_inputs["tops_border_blue"].get_int()
        # колір активації вершини
        self.tops_params[2][0]=self.color_inputs["tops_active_red"].get_int()
        self.tops_params[2][1]=self.color_inputs["tops_active_green"].get_int()
        self.tops_params[2][2]=self.color_inputs["tops_active_blue"].get_int()
        # Радіус вершини
        self.tops_params[3]=self.radius_inputs["top_d"].get_int()
        #Товщина границі
        self.tops_params[4]=self.radius_inputs["top_border"].get_int()
        #перевірка даних
        if self.tops_params[3]<5:
            ctypes.windll.user32.MessageBoxW(0, "Замалий радіус вершини.", 0)
        elif self.tops_params[4]<1:
            ctypes.windll.user32.MessageBoxW(0, "Замала товщина границі вершини.", 0)
        elif self.tops_params[1][0]+self.tops_params[1][1]+self.tops_params[1][2]>650:
            ctypes.windll.user32.MessageBoxW(0, "Занадто світлий колір границі вершини.", 0)
        elif self.links_params[0][0]+self.links_params[0][1]+self.links_params[0][2]>650:
            ctypes.windll.user32.MessageBoxW(0, "Занадто світлий колір ребер.", 0)
        else:
            self.end_function(True, self.tops_params, self.links_params)




    def set_inputs(self):
        #тіло вершини
        self.color_inputs["tops_body_red"]=Input_int_box([20, 60],[30,40],"R:", max_input=255)
        self.color_inputs["tops_body_green"]=Input_int_box([70, 60],[30,40],"G:", max_input=255)
        self.color_inputs["tops_body_blue"]=Input_int_box([120, 60],[30,40],"B:", max_input=255)
        self.color_inputs["tops_body_red"].input=str(self.tops_params[0][0])
        self.color_inputs["tops_body_green"].input=str(self.tops_params[0][1])
        self.color_inputs["tops_body_blue"].input=str(self.tops_params[0][2])
        #колір зв'язку
        self.color_inputs["links_red"]=Input_int_box([20, 130],[30,40],"R:", max_input=255)
        self.color_inputs["links_green"]=Input_int_box([70, 130],[30,40],"G:", max_input=255)
        self.color_inputs["links_blue"]=Input_int_box([120, 130],[30,40],"B:", max_input=255)
        self.color_inputs["links_red"].input=str(self.links_params[0][0])
        self.color_inputs["links_green"].input=str(self.links_params[0][1])
        self.color_inputs["links_blue"].input=str(self.links_params[0][2])
        #колір обводки/тексту
        self.color_inputs["tops_border_red"]=Input_int_box([20, 200],[30,40],"R:", max_input=255)
        self.color_inputs["tops_border_green"]=Input_int_box([70, 200],[30,40],"G:", max_input=255)
        self.color_inputs["tops_border_blue"]=Input_int_box([120, 200],[30,40],"B:", max_input=255)
        self.color_inputs["tops_border_red"].input=str(self.tops_params[1][0])
        self.color_inputs["tops_border_green"].input=str(self.tops_params[1][1])
        self.color_inputs["tops_border_blue"].input=str(self.tops_params[1][2])
        #колір активації вершини
        self.color_inputs["tops_active_red"]=Input_int_box([20, 270],[30,40],"R:", max_input=255)
        self.color_inputs["tops_active_green"]=Input_int_box([70, 270],[30,40],"G:", max_input=255)
        self.color_inputs["tops_active_blue"]=Input_int_box([120, 270],[30,40],"B:", max_input=255)
        self.color_inputs["tops_active_red"].input=str(self.tops_params[2][0])
        self.color_inputs["tops_active_green"].input=str(self.tops_params[2][1])
        self.color_inputs["tops_active_blue"].input=str(self.tops_params[2][2])
        #Радіус вершини
        self.radius_inputs["top_d"]=Input_int_box([20, 340], [30, 40], "Радіус вершини:", max_input=50)
        self.radius_inputs["top_d"].input=str(self.tops_params[3])
        #Товщина границі
        self.radius_inputs["top_border"]=Input_int_box([20, 390], [30, 40], "Товщина границі вершини:", max_input=10)
        self.radius_inputs["top_border"].input = str(self.tops_params[4])


    def left_mouse_click(self, event):
        for i in self.buttons.keys():
            self.buttons[i].clicked(event.pos)
        for i in self.color_inputs.keys():
            self.color_inputs[i].clicked(event.pos)
        for i in self.radius_inputs.keys():
            self.radius_inputs[i].clicked(event.pos)




    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            self.left_mouse_click(event)
        for i in self.color_inputs.keys():
            self.color_inputs[i].update(event)
        for i in self.radius_inputs.keys():
            self.radius_inputs[i].update(event)


    def draw_buttons(self):
        for i in self.buttons.keys():
            self.buttons[i].draw(self.screen)

    def draw_inputs(self):
        for i in self.color_inputs.keys():
            self.color_inputs[i].draw(self.screen)
        for i in self.radius_inputs.keys():
            self.radius_inputs[i].draw(self.screen)

    def draw_text(self):
        myfont = pygame.font.SysFont('Arial', 16)
        textsurface = myfont.render("Основний колір вершини:", False, (0,0,0))
        self.screen.blit(textsurface, [10, 40])
        textsurface = myfont.render("Колір ребер:", False, (0,0,0))
        self.screen.blit(textsurface, [10, 110])
        textsurface = myfont.render("Колір границь вершин/тексту вершин:", False, (0,0,0))
        self.screen.blit(textsurface, [10, 180])
        textsurface = myfont.render("Колір границі активованої вершини:", False, (0, 0, 0))
        self.screen.blit(textsurface, [10, 250])
        textsurface = myfont.render("Інше:", False, (0, 0, 0))
        self.screen.blit(textsurface, [10, 320])

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.draw_buttons()
        self.draw_inputs()
        self.draw_text()
        pygame.display.flip()
