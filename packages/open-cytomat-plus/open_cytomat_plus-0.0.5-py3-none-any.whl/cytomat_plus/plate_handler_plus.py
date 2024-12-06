import subprocess
import sys
import time
import os
from cytomat.plate_handler import PlateHandler
from cytomat.status import OverviewStatus
from cytomat.serial_port import SerialPort
from cytomat.parameters import Parameters
from cytomat.convert_steps import ConvertSteps as CS

class PlateHandlerPlus(PlateHandler):

    def __init__(self, serial_port: SerialPort) -> None:
        self.parameters = Parameters()
        self.parameters.load()
        super().__init__(serial_port)
        self.lid_holder_slot = self.parameters.lid_holder_slot
        self.pipet_station_slot = self.parameters.pipet_station_slot
        self.max_steps_shovel = self.parameters.max_steps_shovel
        self.measurement_slot = self.parameters.measurement_slot
              
    def move_x_to_slot(self, slot: int) -> OverviewStatus:
        """time
        Move along to the given slot (only moves along the x axis)

        Parameters
        ----------
        slot
            The target slot
        """
        return self._PlateHandler__serial_port.issue_action_command(f"ll:xp {slot:03}")
    
    def leave_lid_at_holder(self) -> list[OverviewStatus]:
        if self.parameters.lid_holder_slot != None:
            command_list: list[OverviewStatus]
            command_list = [
                lambda: self.rotate_handler_to_slot(self.lid_holder_slot),
                lambda: self.move_x_to_slot(self.lid_holder_slot),
                lambda: self.move_handler_above_slot_height(self.lid_holder_slot),
                lambda: self.extend_shovel(),
                lambda: self.run_height_in_relative_mm(-15),
                lambda: time.sleep(2),
                lambda: self.retract_shovel(),
                lambda: self.reset_handler_position()]
            return command_list
        else:
            return print("Cup holder not initialized, missing arg type int at the initialisation of Object type CytomatPlus") 
    
    def get_lid_from_holder(self)-> list[OverviewStatus]:
        if self.parameters.lid_holder_slot != None:
            command_list: list[OverviewStatus]
            command_list = [
                lambda: self.rotate_handler_to_slot(self.lid_holder_slot),
                lambda: self.move_x_to_slot(self.lid_holder_slot),
                lambda: self.move_handler_below_slot_height(self.lid_holder_slot),
                lambda: self.extend_shovel(),
                lambda: self.run_height_in_relative_mm(15),
                lambda: time.sleep(2),
                lambda: self.retract_shovel(),
                lambda: self.reset_handler_position()]

            return command_list

    def move_below_slot(self, slot: int)->list[OverviewStatus]:
        command_list: list[OverviewStatus]
        command_list = [
            lambda: self.rotate_handler_to_slot(slot),
            lambda: self.move_x_to_slot(slot),
            lambda: self.move_handler_below_slot_height(slot)]
        return command_list

    def pipet_station(self, rows: int, distance_mm: float, start_mm: float) -> list[OverviewStatus]:
        if (rows * distance_mm) + start_mm > CS.steps_to_mm_shovel(self.max_steps_shovel):
            raise ValueError("The parameters are ot compatible with the Plate handler")
            
        command_list: list[OverviewStatus]
        command_list = [
            lambda: self.move_handler_below_slot_height(self.pipet_station_slot),
            lambda: self.run_shovel_in_relative_mm(start_mm)        
        ]
        for i in range(rows):
            command_list.append(lambda: time.sleep(0.5))
            command_list.append(lambda: self.run_shovel_in_relative_mm(distance_mm))
            command_list.append(lambda: time.sleep(0.5))
            command_list.append(lambda: self.run_height_in_relative_mm(15))
            command_list.append(lambda: time.sleep(0.5))
            command_list.append(lambda: self.run_height_in_relative_mm(-15))
            command_list.append(lambda: time.sleep(0.5))
            
        command_list.append(lambda: self.retract_shovel())
        return command_list

    def do_media_change_from_slot(self, slot: int):
        command_list: list[OverviewStatus]
        first_part = [  lambda: self.move_plate_from_slot_to_handler(slot),
                        lambda: self.leave_lid_at_holder()]

        second_part = self.move_below_slot(slot)

        third_part = self.pipet_station()

        fourth_part = [ lambda: self.get_lid_from_holder(),
                        lambda: self.move_plate_from_handler_to_slot(slot)]

        command_list = first_part + second_part + third_part + fourth_part
        return command_list


    #TODO finisch this func
    def inverted_do_mediachange_from_slot(self, slot: int):
        command_list: list[OverviewStatus]
        command_list = [
            lambda: self.move_plate_from_handler_to_slot(slot)]

    def get_plate_do_measurement_bring_back_plate(self, plate: str, slot_a: int) -> list[OverviewStatus]:
        command_list :list[OverviewStatus]
        command_list = [
            lambda: self.move_plate_from_slot_to_handler(slot_a),
            lambda: self.move_plate_from_handler_to_slot(self.measurement_slot),
            lambda: self.run_foc(plate),
            lambda: self.move_plate_from_slot_to_handler(self.measurement_slot),
            lambda: self.move_plate_from_handler_to_slot(slot_a)]

        return command_list

    def inverted_get_plate_do_measurement_bring_back_plate(self, slot_a: int)->list[OverviewStatus]:
        command_list = [
            lambda: self.move_plate_from_slot_to_handler(slot_a),
            lambda: self.move_plate_from_handler_to_slot(self.measurement_slot),
            lambda: time.sleep(0.1),
            lambda: self.move_plate_from_slot_to_handler(self.measurement_slot),
            lambda: self.move_plate_from_handler_to_slot(slot_a)]
        return command_list

    def move_plate_from_transfer_station_to_slot_v2(self):
        pass

    def inverted_move_plate_from_transfer_station_to_slot_v2(self):
        pass

    def move_plate_from_slot_a_to_slot_b(self, slot_a: int, slot_b:int):
        command_list :list[OverviewStatus]
        command_list = [
            lambda: self.move_plate_from_slot_to_handler(slot_a),
            lambda: self.move_plate_from_handler_to_slot(slot_b)]

        return command_list

    def run_foc(self, plate, _timeout: int =180):
        cmd_l = f'C:\\labhub\\Import\\FOC48.bat {plate}'
        
        try:
            process = subprocess.run(cmd_l, timeout=_timeout, shell = True)
            print("done")

        except subprocess.TimeoutExpired:
            print(" timeout expired")


    def test(self) -> list[OverviewStatus]:
        command_list: list[OverviewStatus]
        command_list = [
            lambda: self.open_transfer_door(),
            lambda: self.close_transfer_door()]
        return command_list

    def test3(self) -> list[OverviewStatus]:
        command_list: list[OverviewStatus]
        command_list = [
            lambda: print(1),
            lambda: print(2),
            lambda: print(3),
            lambda: print(4),
            lambda: print(5),
            lambda: print(6)]

        return command_list

    def inverted_test3(self):
        command_list = [
            lambda: print(6),
            lambda: print(5),
            lambda: print(4),
            lambda: print(3),
            lambda: print(2),
            lambda: print(1)]

        return command_list
