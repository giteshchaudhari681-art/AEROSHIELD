from typing import List, Dict, Any, Tuple
from app.simulation.models import SimulatedObject
from app.infrastructure.db.models import Sensor, SensorStatus
from sqlalchemy.orm import Session
from app.infrastructure.db.session import SessionLocal

class SimulationScenario:
    def __init__(self, name: str):
        self.name = name
        self.objects: List[SimulatedObject] = []
        self.sensors: List[Sensor] = []
        
    def setup(self):
        pass

class BaselineScenario(SimulationScenario):
    def __init__(self):
        super().__init__("baseline")
        
    def setup(self):
        self.objects = [
            SimulatedObject(
                latitude=37.773, longitude=-122.420, altitude=150,
                speed=10.0, heading=45, vertical_speed=0,
                metadata={"rf_emitter": True}
            ),
            SimulatedObject(
                latitude=37.776, longitude=-122.418, altitude=300,
                speed=20.0, heading=180, vertical_speed=-1.0,
                metadata={"rf_emitter": False}
            )
        ]
        db = SessionLocal()
        self.sensors = db.query(Sensor).filter(Sensor.site_id == "site-demo-dt-001", Sensor.is_enabled == True, Sensor.operational_status == SensorStatus.ACTIVE).all()
        db.close()

class SensorDropoutScenario(SimulationScenario):
    def __init__(self):
        super().__init__("sensor_dropout")
        
    def setup(self):
        self.objects = [
            SimulatedObject(latitude=37.775, longitude=-122.419, altitude=100, speed=5.0, heading=90)
        ]
        db = SessionLocal()
        self.sensors = db.query(Sensor).filter(Sensor.site_id == "site-demo-dt-001", Sensor.is_enabled == True).all()
        db.close()
        # High dropout
        self.dropout_override = 0.5

class MultiObjectScenario(SimulationScenario):
    def __init__(self):
        super().__init__("multi_object")
        
    def setup(self):
        db = SessionLocal()
        self.sensors = db.query(Sensor).filter(Sensor.site_id == "site-demo-dt-001", Sensor.is_enabled == True).all()
        db.close()
        self.objects = []
        for i in range(10):
            self.objects.append(SimulatedObject(
                latitude=37.770 + i*0.001,
                longitude=-122.425 + i*0.001,
                altitude=100 + i*10,
                speed=5.0 + i,
                heading=i*30
            ))

SCENARIOS = {
    "baseline": BaselineScenario,
    "sensor_dropout": SensorDropoutScenario,
    "multi_object": MultiObjectScenario
}
