

class Top:
    def __init__(self, id:int=0, pos:list=[0,0], number:int=0):
        self.id=id
        self.position=pos
        self.number=number
        self.active=False


    def set_by_converted_data(self, data):
        self.id=data["id"]
        self.position=data["pos"]
        self.number=data["num"]
        self.active=data["active"]

    def convert_data(self):
        return {"pos":self.position, "num":self.number, "active":self.active, "id":self.id}