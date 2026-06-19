from models import MarkerProduct
from stations import BodyMoldingStation, InkFillingStation, TipInsertionStation, CapAssemblyStation, QualityPackagingStation

class MarkerProductionLine:
    def __init__(self):
        self.stations = [
            BodyMoldingStation(),
            InkFillingStation(),
            TipInsertionStation(),
            CapAssemblyStation(),
            QualityPackagingStation(),
        ]
        self.state = "IDLE"
        self.current_stage = "Waiting"
        self.total_parts = 0
        self.good_parts = 0
        self.defective_parts = 0
        self.last_error = "None"
        self.serial_counter = 0
        self.faulted = False

    def start(self):
        self.state = "PRODUCTIVE"
        self.faulted = False

    def stop(self):
        self.state = "STOPPED"

    def reset(self):
        self.state = "IDLE"
        self.current_stage = "Waiting"
        self.total_parts = 0
        self.good_parts = 0
        self.defective_parts = 0
        self.last_error = "None"
        self.serial_counter = 0
        self.faulted = False

    def produce_one_marker(self):
        if self.state != "PRODUCTIVE":
            return None
        self.serial_counter += 1
        product = MarkerProduct(serial_number=self.serial_counter)
        for station in self.stations:
            self.current_stage = station.name
            product = station.process(product)
            if product.defective:
                self.faulted = True
                self.last_error = product.defect_reason
                break
        self.total_parts += 1
        if product.defective:
            self.defective_parts += 1
            self.state = "FAULTED"
        else:
            self.good_parts += 1
            self.last_error = "None"
            self.faulted = False
        return product

    def state_code(self) -> int:
        return {"IDLE": 0, "PRODUCTIVE": 1, "STOPPED": 2, "FAULTED": 3}.get(self.state, 0)
