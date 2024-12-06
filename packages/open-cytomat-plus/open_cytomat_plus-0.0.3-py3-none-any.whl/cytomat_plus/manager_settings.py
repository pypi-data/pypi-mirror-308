from tkinter import *
from cytomat.utils import lazy_load_config_file
from cytomat.scripts.setup_cytomat import get_config_dir
from .manage_settings.manager_slots import ManagerSlots
from .manage_settings.manager_config_file import ManagerConfigFile
from sqlite3 import IntegrityError
import tkinter.font

class ManagerSettings():
    __root: Toplevel
    def __init__(self, db, root): 
        self.__root = Toplevel(root)
        self.__root.title('Setting Manager')
        self.__root.geometry('1280x720')
        self.__root.withdraw()
        self.__db = db
        
        #from utils file
        self.__config_data_json: dict = lazy_load_config_file()
        #from setup_cytomat file
        self.__config_path = get_config_dir()
        
        self.sync_db_with_config_file()
        self.__root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def get_root(self):
        return self.__root

    def display_window(self):
        self.__root.deiconify()
    
    def create_overview(self):
        self.set_grid_settings()
        self.create_enter_label()
        self.create_button_gui()
        self.create_button_settings()
        self.create_theme_check_box()
        self.__theme_pack = self.set_theme('light')
        self.aplay_theme_settings(self.__theme_pack)
        
    def set_grid_settings(self):
        self.__root.rowconfigure(0, weight = 1)
        self.__root.rowconfigure(1, weight = 2)
        self.__root.columnconfigure(0, weight = 1)
        self.__root.columnconfigure(1, weight = 1)
        self.__root.columnconfigure(2, weight = 1)
        
    def create_enter_label(self):
        font = tkinter.font.Font(family = 'Times New Roman', size = 14)
        
        self.__enter_label = Label(self.__root, text = 'Enter Settings', font=font)
        self.__enter_label.grid(row=0, column=0, sticky = 'ew')
        
        self.__enter_label_gui = Label(self.__root, text = 'Enter Cytomat GUI', font = font)
        self.__enter_label_gui.grid(row = 0, column=1, sticky='ew')
        
    def create_button_settings(self):
        self.__button_settings = Button(self.__root, text = 'Enter', command = self.settings_button_callback)
        self.__button_settings.grid(row = 1, column=0, ipadx = 40, ipady = 10, sticky='n')
        
    def create_button_gui(self):
        self.__button_gui = Button(self.__root, text = 'Enter', command = self.gui_button_callback)
        self.__button_gui.grid(row = 1, column=1, ipadx = 40, ipady = 10, sticky='n')
        
    def settings_button_callback(self):
        self.create_top_level_window()
    
    def gui_button_callback(self):
        self.__root.withdraw()
        
    def on_close(self):
        #self.no_button_callback()
        self.__root.destroy()
        
    def create_theme_check_box(self):
        self.check_box_var = BooleanVar()
        self.__theme_check_box = Checkbutton(self.__root, text = 'Dark Mode', variable= self.check_box_var, command = self.theme_check_box_callback)
        self.__theme_check_box.grid(row = 0, column=2)
        
    def theme_check_box_callback(self):
        if self.check_box_var.get():
            self.__theme_pack = self.set_theme('dark')
        else:
            self.__theme_pack = self.set_theme('light')
            
        self.aplay_theme_settings(self.__theme_pack)
    
    def set_theme(self, theme):
        theme_pack = {}
        if theme == 'dark':
            theme_pack['family'] = 'dark'
            theme_pack['entry'] = '#616161'
            theme_pack['button'] = '#424242'
            theme_pack['fg'] = 'white'
            theme_pack['bg'] = '#454545'
            theme_pack['header'] = '#707070'
            
        else:
            theme_pack['family'] = 'light'
            theme_pack['entry'] = 'lightgrey'
            theme_pack['button'] = 'white'
            theme_pack['fg'] = 'black'
            theme_pack['bg'] = '#E5E5E5'
            theme_pack['header'] = '#BDBDBD'
            
        return theme_pack
    
    def aplay_theme_settings(self, theme_pack: dict):
        bg = theme_pack['bg']
        fg = theme_pack['fg']
        entry = theme_pack['entry']
        button = theme_pack['button']
        
        self.__root.config(bg=bg)
        self.__button_settings.config(bg = button, fg = fg)
        self.__button_gui.config(bg = button, fg = fg)
        self.__enter_label.config(fg = fg, bg = bg)
        self.__enter_label_gui.config(bg = bg, fg = fg)
        
        try:
            self.top_level.applay_theme_pack(theme_pack=self.__theme_pack)
            
        except Exception:
            pass
            
    def create_top_level_window(self):
        self.top_level = ManagerSettingsTop(root = self.__root, config_data=self.__config_data_json, config_path=self.__config_path, db = self.__db)
        self.top_level.create_overview()
        self.top_level.applay_theme_pack(theme_pack=self.__theme_pack)
    
    def sync_db_with_config_file(self):
        for key, value in self.__config_data_json.items():
            if not 'slot' in key:
                continue
            
            if not value:
                continue
            
            try:    
                self.__db.insert_new_row(slot = value, role = 1)
                 
            except IntegrityError:
                continue


        #Create Rows to Setup Slots
        
    def submit_callback(self):
        pass
    
    
class ManagerSettingsTop():
    __root: Toplevel
    def __init__(self, root, db, config_path, config_data):
        self.__root = Toplevel(root)
        self.__root.title('Settings')
        self.__root.geometry('1920x1080')
        
        self.__db = db
        self.__config_data_json = config_data
        self.__config_path = config_path
        self.setup_frames()
        
    def get_root(self):
        return self.__root
        
    def create_overview(self):
        self.__manager_config = ManagerConfigFile(root = self.__left_frame, data = self.__config_data_json, config_directory_path = self.__config_path, db=self.__db)
        self.__manager_slots = ManagerSlots(root = self.__right_frame, db = self.__db)
        
        self.__manager_config.create_overview()
        self.__manager_slots.create_overview()
        
        
    def setup_frames(self):
        self.__left_frame = Frame(self.__root)
        self.__left_frame.grid(row = 0, column = 0, sticky = 'nsew')
                
        self.__right_frame = Frame(self.__root, bg = 'lightblue')
        self.__right_frame.grid(row = 0, column = 1, sticky = 'nsew')
        
        self.__root.columnconfigure(0, weight=1)
        self.__root.columnconfigure(1, weight = 1)
        self.__root.rowconfigure(0, weight = 1)
    
    def applay_theme_pack(self, theme_pack):
        self.__theme_pack = theme_pack
        self.__manager_config.aplay_theme_pack(theme_pack = self.__theme_pack)
        self.__manager_slots.aplay_theme_pack(theme_pack = self.__theme_pack)