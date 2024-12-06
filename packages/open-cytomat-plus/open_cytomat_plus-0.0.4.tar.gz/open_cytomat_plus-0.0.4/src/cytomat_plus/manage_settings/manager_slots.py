from tkinter import *
from cytomat_plus.db import DB

class ManagerSlots():
    __root: Frame
    __db: DB
    def __init__(self, root, db):
        self.__root = root
        self.__db = db
        self.__row_obj_list = []
        
    def create_overview(self):
        self.set_grid_settings()
        self.create_header()
        self.create_entry_area()
    
    def create_header(self):
        self.__header_slots = Label(self.__root, text = "Set the Slots wich should be used", font = ('Helvetica', 20), pady = 1, padx = 1, relief='solid')
        self.__header_slots.grid(row = 0, column=0, columnspan = 4, sticky='nsew', ipady = 30)
        
    def create_entry_area(self):
        y = 12
        
        self.__entry_bottom = Entry(self.__root, textvariable = 'bottom', justify = 'center')
        self.__entry_bottom.grid(row = 1, column = 0, sticky = 'nsew', ipady = y)
        
        self.__middle_label = Label(self.__root, text = '-', font=('Helvetica', 14))
        self.__middle_label.grid(row= 1, column = 1, sticky = 'nsew', ipady = y)
        
        self.__entry_upper = Entry(self.__root, textvariable = 'upper', justify = 'center')
        self.__entry_upper.grid(row = 1, column = 2, sticky = 'nsew', ipady = y)
    
        self.__enter_button = Button(self.__root, text = 'Enter', command = self.enter_button_callback)
        self.__enter_button.grid(row = 1, column = 3, sticky = 'nsew', ipady = y)
    
    def set_grid_settings(self):
        #self.__root.rowconfigure(0, weight=2)
        #self.__root.rowconfigure(1, weight=1)
        self.__root.rowconfigure(2, weight=1)
        self.__root.rowconfigure(3, weight=2)
        self.__root.rowconfigure(4, weight=2)
        self.__root.columnconfigure(0, weight = 2)
        self.__root.columnconfigure(1, weight = 1)
        self.__root.columnconfigure(2, weight = 2)
        self.__root.columnconfigure(3, weight = 1)
        
    def aplay_theme_pack(self, theme_pack: dict):
        self.__theme_pack = theme_pack
        bg = theme_pack['bg']
        fg = theme_pack['fg']
        entry = theme_pack['entry']
        button = theme_pack['button']
        header = theme_pack['header']
        
        self.__root.config(bg = bg)
        self.__header_slots.config(bg=header, fg = fg)
        self.__middle_label.config(bg = bg, fg = fg)
        self.__entry_upper.config(bg = entry, fg = fg)
        self.__entry_bottom.config(bg = entry, fg = fg)
        self.__enter_button.config(bg = button, fg = fg)
        
        for row in self.__row_obj_list:
            row: SlotsRow
            row.aplay_theme_pack(theme_pack=self.__theme_pack)
        
    def enter_button_callback(self):
        entry_bottom = self.__entry_bottom.get()
        entry_upper = self.__entry_upper.get()
        self.__entry_bottom.delete(0, END)
        self.__entry_upper.delete(0, END)
        
        if not self.is_entry_valid(entry_bottom, entry_upper):
            return
        
        entry_bottom = int(entry_bottom)
        entry_upper = int(entry_upper)
        
        kind_of_entry = self.kind_of_entry(entry_bottom, entry_upper)
         
    
    def is_entry_valid(self, entry_bottom: str, entry_upper: str):
        if not entry_bottom.isdigit() or not entry_upper.isdigit():
            return
        
        if int(entry_upper) < int(entry_bottom):
            return
        
        print("entry valid")
        return True
    
    def kind_of_entry(self, entry_bottom: int, entry_upper: int):
        pass
    
    def merge_entries():
        pass
    
class SlotsRow():
    def __init__(self) -> None:
        pass
    
    def aplay_theme_pack(self, theme_pack):
        pass