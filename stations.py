import random
from abc import ABC, abstractmethod
from models import MarkerProduct

class Station(ABC):
    def __init__(self, name: str, defect_probability: float):
        self.name = name
        self.defect_probability = defect_probability

    def has_defect(self) -> bool:
        return random.random() < self.defect_probability

    @abstractmethod
    def process(self, product: MarkerProduct) -> MarkerProduct:
        pass

class BodyMoldingStation(Station):
    def __init__(self):
        super().__init__("Body Molding", 0.06)

    def process(self, product: MarkerProduct) -> MarkerProduct:
        product.add_history("Marker body molded")
        if self.has_defect():
            product.defective = True
            product.defect_reason = "Cracked marker body detected"
        else:
            product.body_molded = True
        return product

class InkFillingStation(Station):
    def __init__(self):
        super().__init__("Ink Reservoir Filling", 0.07)

    def process(self, product: MarkerProduct) -> MarkerProduct:
        product.add_history("Ink reservoir filled")
        if self.has_defect():
            product.defective = True
            product.defect_reason = "Ink reservoir underfilled"
        else:
            product.reservoir_filled = True
        return product

class TipInsertionStation(Station):
    def __init__(self):
        super().__init__("Tip Insertion", 0.05)

    def process(self, product: MarkerProduct) -> MarkerProduct:
        product.add_history("Writing tip inserted")
        if self.has_defect():
            product.defective = True
            product.defect_reason = "Tip missing or misaligned"
        else:
            product.tip_inserted = True
        return product

class CapAssemblyStation(Station):
    def __init__(self):
        super().__init__("Cap Assembly", 0.04)

    def process(self, product: MarkerProduct) -> MarkerProduct:
        product.add_history("Cap attached")
        if self.has_defect():
            product.defective = True
            product.defect_reason = "Cap not locked correctly"
        else:
            product.cap_attached = True
        return product

class QualityPackagingStation(Station):
    def __init__(self):
        super().__init__("Quality Control and Packaging", 0.03)

    def process(self, product: MarkerProduct) -> MarkerProduct:
        product.add_history("Quality check completed")
        if self.has_defect():
            product.defective = True
            product.defect_reason = "Final leak or print quality failure"
        if not product.defective:
            product.packaged = True
            product.add_history("Marker packaged")
        return product
