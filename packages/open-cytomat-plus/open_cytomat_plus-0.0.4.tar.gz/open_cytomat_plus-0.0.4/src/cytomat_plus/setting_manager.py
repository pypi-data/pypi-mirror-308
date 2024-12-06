from tkinter import *
from cytomat.utils import lazy_load_config_file
from cytomat.scripts.setup_cytomat import get_config_dir
from cytomat_plus.db import DB
import json
import re

class SettingManager():
    def __init__(self):
        self.__root = Tk()
        self.__root.title('Setting Manager')
        self.__root.geometry('1920x1080')
 
        self.config_data_json: dict = lazy_load_config_file()
        self.__total_columns_left = 3
    
    def get_root(self):
        return self.__root
    
    def setup_frames(self):
        self.__left_frame = Frame(self.__root)
        self.__left_frame.grid(row = 0, column = 0, sticky = 'nsew')
        self.__root.columnconfigure(0, weight=1)
                
        self.__right_frame = Frame(self.__root, bg = 'lightblue')
        self.__right_frame.grid(row = 0, column = 1, sticky = 'nsew')
        self.__root.columnconfigure(1, weight = 1)
        
        self.__root.rowconfigure(0, weight = 1)    

    def create_header_config(self):
        self.__header_config = Label(self.__left_frame, text = "Set specific parameters for the Cytomat", font=('Helvetica', 20), pady = 1, padx = 1)
        self.__header_config.grid(row = 0, column = 0, sticky = 'ns', columnspan = self.__total_columns_left)

    def create_left_frame_objects(self):
        self.__left_frame.grid_columnconfigure(0, weight=2)
        self.__left_frame.grid_columnconfigure(1, weight=2)
        self.__left_frame.grid_columnconfigure(2, weight=1)
        for index, (key, value) in enumerate(self.config_data_json.items()):    
            SettingsConfigFile(root = self.__left_frame, setting_manager = self, key = key, value = value, type = type(value), row_idx = index + 1, data=self.config_data_json)

    def create_right_frame_object(self):
        SettingsSlots(root = self.__right_frame)

    def create_overview(self):
        self.setup_frames()
        self.create_header_config()
        
        self.create_left_frame_objects()
        self.create_right_frame_object()

        #Create Rows to Setup Slots
        
    def submit_callback(self):
        pass

"""
This Class displays the left side of the window
"""

class SettingsConfigFile():
    __root: Tk
    def __init__(self, root, setting_manager, key, value, type, row_idx, data):
        self.setting_manager = setting_manager
        self.key = key
        self.value = value
        self.type = type
        self.__root = root
        self.row_idx = row_idx
        self.data = data
        self.create_row()

    def create_row(self):
        self.__root.rowconfigure(self.row_idx, weight =1)
        self.create_label()
        self.create_entry()
        self.create_enter_button()

    def create_label(self):
        self.__row_label = Label(self.__root, text = str(self.key), font=('Helvetica', 14), relief='solid',  pady = 5, padx = 1)
        self.__row_label.grid(row=self.row_idx, column = 0, sticky='nsew', ipadx = len(str(self.value)))

    def create_entry(self):
        entry_text = StringVar(value = self.value)
        self.__row_entry = Entry(self.__root, textvariable = entry_text)
        self.__row_entry.grid(row = self.row_idx, column = 1, sticky='nsew', ipadx = len(str(self.value)))

    def create_enter_button(self):
        self.enter_button = Button(self.__root, text = "Enter", command = self.enter_button_callback)
        self.enter_button.grid(row = self.row_idx, column = 2, sticky='nsew', ipadx = len('entry'))
        
    def enter_button_callback(self):
        entry = self.__row_entry.get()
        
        print(f"""  entry: {entry}
                    entry is digit: {entry.isdigit()}
                    row type: {self.type}""")
        
        if entry.isdigit() and self.type is not int:
            return
        
        if not entry.isdigit() and self.type is int:
            return
        
        if entry.isdigit() and self.type is int:
            entry = int(entry)
            self.data[self.key] = entry
            
        if not entry.isdigit() and self.type is str:
            print("COM_port_entry")
            #regular expression if the entry is for the COMPort
            comp = r"^COM\d+$" 
            
            if bool(re.match(comp, entry)) is False:
                return print("invalid COMPort")
            
            self.data[self.key] = entry
            
            
            
class SettingsSlots():
    __root: Frame
    def __init__(self, root):
        self.__root = root
        self.__db = DB()
        self.__slots_roled = self.__db.get_roled_slots()
        self.__slots_unroled = self.__db.get_unroled_slots()
        if len(self.__slots_unroled) > 0:
            print(self.__slots_unroled)
            self.__entry_dict = self.create_entry_dict()
            self.aplay_changes_display()
        else: 
            self.__entry_dict = {}
        self.create()
        
    def create(self):
        self.set_grid_settings()
        self.create_header()
        self.create_entry_area()    
    
    def create_header(self):
        self.__header_slots = Label(self.__root, text = "Set the Slots wich should be used", font = ('Helvetica', 20), pady = 1, padx = 1)
        self.__header_slots.grid(row = 0, column=0, columnspan = 4, sticky='nsew')
        
    def create_entry_area(self):
        self.__entry_bottom = Entry(self.__root, textvariable = 'bottom')
        self.__entry_bottom.grid(row = 1, column = 0, sticky = 'nsew')
        
        self.__middle_label = Label(self.__root, text = '-', font=('Helvetica', 18))
        self.__middle_label.grid(row= 1, column = 1, sticky = 'nsew')
        
        self.__entry_upper = Entry(self.__root, textvariable = 'upper')
        self.__entry_upper.grid(row = 1, column = 2, sticky = 'nsew')
    
        self.__enter_button = Button(self.__root, text = 'Enter', command = self.enter_button_callback)
        self.__enter_button.grid(row = 1, column = 3, sticky = 'nsew')
        
    def set_grid_settings(self):
        self.__root.columnconfigure(0, weight = 2)
        self.__root.columnconfigure(1, weight = 1)
        self.__root.columnconfigure(2, weight = 2)
        self.__root.columnconfigure(3, weight = 1)
    
    """
    """
        
    def initialze_entry_object(self, sequence: list, db: DB):
        obj = Entries(sequence = sequence, db = db)
        return obj
    
    def aplay_changes_db(self):
        for key in self.__entry_dict.keys():
            start, end = key
            for slot in range(start, end + 1): 
                self.__db.insert_new_row(slot = slot, plate = None, role = 0, occupied = 0, current_plate_id = None)

        self.__slots_unroled = self.__db.get_unroled_slots()
        
    def aplay_changes_display(self):
        for index, key in enumerate (self.__entry_dict.keys()):
            obj: Entries = self.__entry_dict[key][1]
            obj.display_entry(row = index + 2, root = self.__root)
    
    def enter_button_callback(self):
        is_valid = self.is_entry_valid(entry_bottom = self.__entry_bottom.get(), entry_upper = self.__entry_upper.get())
        
        if not is_valid:
            return
        
        kind = self.kind_of_entry()
        if kind == 'new':
            self.create_new_entry()
            
        if kind == 'merge':
            self.merge_entries()
            
        self.aplay_changes_db()
        self.aplay_changes_display()
        
        
        """
        This function iterates through all the slots already in use for regular plates and searches for contiguous sequences.
        For each found sequence, it creates an Entries object (which is initialized with the sequence) and saves it in a dictionary
        using the start and end of the sequence as the key. It returns that dictionary.
        """
    def create_entry_dict(self)->dict:
        entry_dict = {}
        curr_subsequence = []
        for i in range (1, len(self.__slots_unroled)):
            if  self.__slots_unroled[i] == self.__slots_unroled[i-1] + 1:
                curr_subsequence.append(i) 
            else:
                key = (curr_subsequence[0], curr_subsequence[-1])
                entry_dict[key] = (curr_subsequence, self.initialze_entry_object(sequence=curr_subsequence, db = self.__db))
                curr_subsequence = []
                
        #last entry        
        key = (curr_subsequence[0], curr_subsequence[-1])
        entry_dict[key] = (curr_subsequence, self.initialze_entry_object(sequence=curr_subsequence, db = self.__db))
        
        return entry_dict
    
    def is_entry_valid(self, entry_bottom, entry_upper)-> bool:
        
        #checks if both of the entrys are positive integers
        if entry_bottom.isdigit() == False or entry_upper.isdigit() == False:
            return False
        
        if int(entry_bottom) > int(entry_upper):
            return False
        
        self.__entry_list = self.create_entry_list(int(entry_bottom), int(entry_upper))
           
        #checks if any of the numbers tryning to set as a Slot is already roled.
        if self.is_intersection_roled(self.__entry_list):
            return False
            
        return True
    
    """
    return 'merge' if there is an intersection or a countinuos sequence in the new entry and the used slots in db, else 'new' for new entry obj
    """
    def kind_of_entry(self)->str:
        if self.is_intersection_used(self.__entry_list):
            return 'merge'
        else: 
            return 'new'
        
    """Return a boolean indicating whether there is at least one element with a non-zero role that is included
       in the list of slots being attempted to set.
    """
        
    def is_intersection_roled(self, entry_list: list)->bool:
        return bool(set(entry_list) & set(self.__slots_roled))
    
    def is_intersection_used(self, entry_list: list)->bool:
        if not self.__slots_unroled:
            return False
        
        if bool(set(entry_list) & set(self.__slots_unroled)):
            return True
        
        min_entry, max_entry = min(entry_list), max(entry_list)
        min_slot, max_slot = min(self.__slots_unroled), max(self.__slots_unroled)

        if max_entry + 1 == min_slot or max_slot + 1 == min_entry:
            return True
        
        return False
        
    def create_entry_list(self, entry_bottom: int, entry_upper: int):
        entry_list = []
        for i in range(entry_bottom, entry_upper+1):
            entry_list.append(i)
        return entry_list
    
    """
    overlapping entries like 1-4 and 2-5 have to be merged. 
    """
    def merge_entries(self):
        start, end = self.__entry_list[0], self.__entry_list[-1]
        keys_to_remove = []
        
        for key in list(self.__entry_dict.keys()):
            seq_start, seq_end = key
            
            #checks if new sequence is identical to an old one or an other sequence contains the new one
            if start >= seq_start and end <= seq_end:
                return None
            
            #checks if new sequence is contains an other sequence 
            if start <= seq_start and end >= seq_end:
                print("hey2")
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del self.__entry_dict[key] 

        #getting all overlapping sequences
        overlapping_keys = []
        for key in list(self.__entry_dict.keys()):
            seq_start, seq_end = key
            if (end >= seq_start or start <= seq_end):
                overlapping_keys.append(key)
        
        merged_list = self.__entry_list.copy()
        for key in overlapping_keys:
            merged_list += self.__entry_dict[key][0]
            del self.__entry_dict[key]
            
        merged_list = sorted(set(merged_list))
        new_key = (merged_list[0], merged_list[-1])
        
        self.__entry_dict[new_key] = (merged_list, self.initialze_entry_object(sequence = merged_list.copy(), db = self.__db))
        self.__slots_unroled = sorted(set(self.__slots_unroled + merged_list))
        
    def create_new_entry(self):
        start, end = self.__entry_list[0], self.__entry_list[-1]
        
        new_key = (start, end)
        self.__entry_dict[new_key] = (self.__entry_list, self.initialze_entry_object(sequence = self.__entry_list(), db=self.__db))
        
        self.__slots_unroled += sorted(set(self.__slots_unroled + self.__entry_list.copy()))
        
   
    def check_for_current_slots():
        pass        
    
    def update_overview(self):
        pass
    
class Entries():
    __DB: DB
    def __init__(self, sequence, db):
        self.sequence = sequence
        self.__start = sequence[0]
        self.__end = sequence[-1]
        self.__db = db

    def display_entry(self, row, root: Frame):
        row = row +2
        root.columnconfigure(0, weight = 2)
        root.columnconfigure(1, weight = 1)
        root.rowconfigure(row, weight = 1)
        self.create_label(row = row, root = root)
        self.create_delete_button(row = row, root = root)
        
    def create_label(self, row, root: Frame):
        self.__label = Label(root, text = f"{self.__start} - {self.__end}", font = ('Helvetica', 20), relief='solid')
        self.__label.grid(row = row, column = 0, sticky= 'nsew')
        
    def create_delete_button(self, row, root: Frame):
        self.__delete_Button = Button(root, text = "Delete Entry", command = self.delete_button_callback)
        self.__delete_Button.grid(row = row, column = 1, sticky='nsew')
        
    def delete_button_callback(self):
        print("Delete")

manager = SettingManager()
manager.create_overview()
root = manager.get_root()
root.mainloop()