from typing import Dict, Type
from .generators.base import SensorSimulator

class SensorSimulatorRegistry:
    def __init__(self):
        self._simulators: Dict[str, Type[SensorSimulator]] = {}

    def register(self, sensor_type: str, simulator_class: Type[SensorSimulator]):
        self._simulators[sensor_type] = simulator_class

    def get(self, sensor_type: str) -> Type[SensorSimulator]:
        if sensor_type not in self._simulators:
            raise ValueError(f"No simulator registered for sensor type: {sensor_type}")
        return self._simulators[sensor_type]

    def list(self):
        return list(self._simulators.keys())

simulator_registry = SensorSimulatorRegistry()

from .generators.radar import RadarSimulator
from .generators.rf import RFSimulator
from .generators.eo_ir import EOIRSimulator
from .generators.acoustic import AcousticSimulator

simulator_registry.register("RADAR", RadarSimulator)
simulator_registry.register("RF", RFSimulator)
simulator_registry.register("EO_IR", EOIRSimulator)
simulator_registry.register("ACOUSTIC", AcousticSimulator)
