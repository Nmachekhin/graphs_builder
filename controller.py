from model import *
from file_servise import *
import ctypes


class Controller():
    def __init__(self):
        self.model=Model()

    def is_empy(self):
        return self.model.is_empty()

    def save_state(self, tops_params, links_params):
        File.save_state(self.get_all_tops(), self.get_all_links(), tops_params, links_params)

    def load_state(self):
        self.model.delete_state()
        try:
            new_tops, new_links, tops_params, links_params = File.load_state()
            self.model.set_loaded_tops(new_tops)
            self.model.set_loaded_links(new_links)
            return [self.get_all_tops(),self.get_all_links(), tops_params, links_params]
        except Exception as e:
            print("Error: "+str(e))
            ctypes.windll.user32.MessageBoxW(0, "Помилка! Перевірте цілісність файлу!", 0)
            self.model.delete_state()
            return [[],[], [], []]


    def left_click_on_empty(self, click_pos:list):
        top = self.model.new_top(click_pos)
        return [top.convert_data()]

    def get_all_tops(self):
        tops=[]
        for i in self.model.tops.keys():
            tops.append(self.model.tops[i].convert_data())
        return tops

    def get_all_links(self):
        links=[]
        for i in self.model.links.keys():
            links.append(self.model.links[i].convert_data())
        return links

    def top_click(self, id:int, pointing_link_option=False, link_has_weight=False, weight=0):
        if self.model.active_top==None:
            self.model.activate_top(id)
        else:
            self.model.build_link(id, pointing_link_option,link_has_weight, weight)
        return [self.get_all_tops(), self.get_all_links()]

    def right_click_on_top(self, id:int):
        self.model.delete_links_near_top(id)
        self.model.delete_top(id)
        return [self.get_all_tops(), self.get_all_links()]
