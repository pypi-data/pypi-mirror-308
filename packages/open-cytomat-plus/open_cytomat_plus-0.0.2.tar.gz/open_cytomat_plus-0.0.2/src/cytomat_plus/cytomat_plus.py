from cytomat.cytomat import Cytomat
from cytomat.status import OverviewStatus
from .plate_handler_plus import PlateHandlerPlus
from .db import DB
from typing import Union
#from ws_barcode_scanner import BarcodeScanner
import time


#current firmware settings: left stack 1-21, right stack 22-42
class CytomatPlus(Cytomat):
    plate_handler: PlateHandlerPlus
    
    def __init__(self, serial_port: str):
        super().__init__(serial_port)
        self.plate_handler = PlateHandlerPlus(self._Cytomat__serial_port)
        self.db = DB()
        self.execute_error = None
        print("cytomat")
        #self.scanner = BarcodeScanner("COM3")

    def wait_until_not_busy(self, timeout: float  = 30, poll_intervall: float = 0.05):
        status = self.overview_status
        max_time = timeout
        start_time = time.time()
        while status.busy:
            if (time.time()-start_time) >= max_time:
                raise TimeoutError(f"Device still busy after {max_time} seconds")
            time.sleep(poll_intervall)
            status = self.overview_status

    def execute(self, command_list: Union[list[OverviewStatus], OverviewStatus], timeout: float = 30, poll_interval: float = 0.5)-> OverviewStatus:
        if not isinstance(command_list, list):
            command_list = [command_list]

        for command in command_list:
            self.wait_until_not_busy(timeout, poll_interval)
            try:
                command()
                self.wait_until_not_busy(timeout = timeout, poll_intervall = poll_interval)
            except Exception as e:
                self.plate_handler.initialize()

    def read_barcode(self):
        self.scanner.query_for_codes()

    def get_status(self):
        return self.overview_status