import pygame
import ctypes
from change_parameters_window import *
from int_input_box import *
from view_button import *
from view_link import *

pygame.init()

class View():
    def __init__(self, controller,
                 tops_params=[[0, 255, 255], [0, 0, 0], [255, 0, 0], 15, 2],  # body_color, border_color, active_border_color, radius, border
                 links_params=[[0, 0, 0], 10]):# body_color, arrow_len
        self.controller=controller
        self.screen_wid=1000
        self.screen_hei=700
        self.control_surface_hei=300
        self.control_surface_wid=150
        self.screen=pygame.display.set_mode([self.screen_wid,self.screen_hei])
        self.set_parameters_mode=False
        self.parameters_window = Parameters_window(self.screen_wid, self.screen_hei, self.screen, self.end_of_changing_parameters, tops_params, links_params)
        self.top_params=tops_params
        self.link_params=links_params
        self.tops= {}
        self.links={}
        self.buttons={}
        self.input_box=None
        self.set_control_atributes()


    def set_control_atributes(self):
        self.buttons["pointing_btn"]=Button(None,[self.screen_wid-self.control_surface_wid+5, 10],[140,20], ["Спрямувати зв'язки", "Не спрямовувати зв'язки"])
        self.buttons["has_weight_btn"]=Button(None,[self.screen_wid-self.control_surface_wid+5, 40],[140,20], ["Додати зв'язкам вагу", "Не додавати зв'язкам вагу"])
        self.buttons["save_as_btn"]=Button(self.save_state,[self.screen_wid-self.control_surface_wid+5, 120],[140,20], ["Зберегти як"])
        self.buttons["load_btn"]=Button(self.load_state,[self.screen_wid-self.control_surface_wid+5, 150],[140,20], ["Завантажити"])
        self.buttons["change_parameters_btn"]=Button(self.change_parameters, [self.screen_wid-self.control_surface_wid+5, 180],[140,20], ["Змінити параметри"])
        self.input_box=Input_int_box([self.screen_wid-self.control_surface_wid+5, 70],[140,40],"Вага зв'язку:")


    def save_state(self):
        self.controller.save_state(self.top_params, self.link_params)

    def change_parameters(self):
        if not self.controller.is_empy():
            ctypes.windll.user32.MessageBoxW(0, "За для правильного відображення, міняти параметри можа лише на чистому полі.", 0)
        else:
            self.set_parameters_mode = True

    def end_of_changing_parameters(self, save, tops_params=[], links_params=[]):
        self.set_parameters_mode=False
        if save:
            self.top_params=tops_params
            self.link_params=links_params



    def load_state(self):
        data=self.controller.load_state()
        self.tops=self.build_top_objects(data[0])
        self.links=self.build_link_objects(data[1])
        if len(data[2])==5:
            self.top_params=data[2]
        if len(data[3])==2:
            self.link_params=data[3]


#<draw objects>

    def draw_links(self):
        for i in self.links.keys():
            link=self.links[i]
            self.tops[link.end_id].set_parameters(self.top_params)
            self.tops[link.start_id].set_parameters(self.top_params)
            link.set_parameters(self.link_params)
            link.draw(self.screen, self.tops[link.start_id], self.tops[link.end_id])


    def draw_control_surface(self):
        pygame.draw.rect(self.screen, (0,0,0), [self.screen_wid-self.control_surface_wid, 0,self.control_surface_wid, self.control_surface_hei])
        pygame.draw.rect(self.screen, (255,255,255), [self.screen_wid-self.control_surface_wid+1, 0,self.control_surface_wid, self.control_surface_hei-1])


    def draw_buttons(self):
        for i in self.buttons.keys():
            self.buttons[i].draw(self.screen)


    def draw_tops(self):
        for i in self.tops.keys():
            self.tops[i].set_parameters(self.top_params)
            self.tops[i].draw(self.screen)


    def draw_canvas(self):
        self.screen.fill((255, 255, 255))
        self.draw_control_surface()
        self.draw_buttons()
        self.input_box.draw(self.screen)
        self.draw_links()
        self.draw_tops()
        pygame.display.flip()

# </draw objects>

    def object_pressed(self, click_pos, mouse_btn):
        if mouse_btn==0:
            for i in self.buttons.keys():
                if self.buttons[i].clicked(click_pos):
                    return i
            if self.input_box.clicked(click_pos):
                return self.input_box.id
        for i in self.tops.keys():
            top_clicked=self.tops[i].is_clicked(click_pos)
            if top_clicked!=None:
                return top_clicked
        if click_pos[0]>=self.screen_wid-self.control_surface_wid-self.top_params[4] \
                and click_pos[1]<=self.control_surface_hei+self.top_params[4]:
            return "near"
        return "clean"


    def build_top_objects(self, data:list=[]):
        tops={}
        for i in data:
            new_top=View_top(i)
            tops|={new_top.id:new_top}
        return tops

    def build_link_objects(self, data:list=[]):
        links={}
        for i in data:
            new_link=View_link(i)
            links|={new_link.id:new_link}
        return links

    def right_mouse_click(self, click_pos):
        pressed_object=self.object_pressed(click_pos, 2)
        if pressed_object in self.tops.keys():
            data=self.controller.right_click_on_top(pressed_object)
            self.tops=self.build_top_objects(data[0])
            self.links=self.build_link_objects(data[1])


    def left_mouse_click(self, click_pos):
        pressed_object=self.object_pressed(click_pos, 0)
        if pressed_object=="clean":
            self.tops=self.tops|self.build_top_objects(self.controller.left_click_on_empty(click_pos))
        elif pressed_object in self.tops.keys():
            data=self.controller.top_click(pressed_object, self.buttons["pointing_btn"].is_toggled, self.buttons["has_weight_btn"].is_toggled, self.input_box.get_int())
            self.tops=self.build_top_objects(data[0])
            self.links=self.build_link_objects(data[1])


    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if self.set_parameters_mode:
                self.parameters_window.event_handler(event)
            else:
                if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                    self.left_mouse_click(list(event.pos))
                if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_RIGHT:
                    self.right_mouse_click(list(event.pos))
                self.input_box.update(event)
        if self.set_parameters_mode:
            self.parameters_window.draw()
        else:
            self.draw_canvas()
        return False