import win32ui
import win32con
import json


class File():
    @staticmethod
    def save_state(tops, links):
        path=File.get_saving_path()
        if path!="":
            file=open(path+".graph","w")
            file.write(json.dumps({"tops":tops, "links":links}))
            file.close()


    @staticmethod
    def load_state():
        path=File.get_loading_path()
        if path!="":
            file=open(path,"r")
            data=json.loads(file.read())
            file.close()
            return [data["tops"], data["links"]]
        return [[],[]]


    @staticmethod
    def get_saving_path():
        openFlags = win32con.OFN_OVERWRITEPROMPT | win32con.OFN_FILEMUSTEXIST
        dialog = win32ui.CreateFileDialog(0, None, None, openFlags, "Graph files (*.graph)|*.graph||")
        dialog.SetOFNInitialDir(r'C:')
        dialog.DoModal()
        return dialog.GetPathName()

    @staticmethod
    def get_loading_path():
        dialog = win32ui.CreateFileDialog(1, None, None, 0, "Graph files (*.graph)|*.graph||")
        dialog.SetOFNInitialDir(r'C:')
        dialog.DoModal()
        return dialog.GetPathName()