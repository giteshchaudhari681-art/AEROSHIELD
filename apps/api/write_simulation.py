import os

base_dir = "d:/SEVA/apps/api/app/simulation"

files = {
    "__init__.py": """from .runtime import simulation_runtime
""",

    "registry.py": """from typing import Dict, Type
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
""",

    "generators/base.py": """from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from app.infrastructure.db.models import Sensor
from app.simulation.models import SimulatedObject
import random
from datetime import datetime, timezone
import math

class SensorSimulator(ABC):
    def __init__(self, sensor: Sensor, random_gen: random.Random):
        self.sensor = sensor
        self.random = random_gen
        self.id = sensor.id
        
        # Parse sensor config if it has geometry
        self.lat = 0.0
        self.lon = 0.0
        # For simplicity, extract coordinates manually or assume they are passed
        # This is a bit tricky without PostGIS loaded in memory, but we can store them in scenario or extract from WKT
        if sensor.location and isinstance(sensor.location, str) and "POINT" in sensor.location:
            try:
                coords = sensor.location.split("(")[1].split(")")[0].split(" ")
                self.lon = float(coords[0])
                self.lat = float(coords[1])
            except:
                pass
                
        self.coverage_radius_m = 10000.0 # Default 10km
        self.dropout_probability = 0.05

    def _distance_m(self, obj: SimulatedObject) -> float:
        # Haversine
        R = 6371e3
        phi1 = math.radians(self.lat)
        phi2 = math.radians(obj.latitude)
        dphi = math.radians(obj.latitude - self.lat)
        dlambda = math.radians(obj.longitude - self.lon)
        
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
        
    def _bearing_deg(self, obj: SimulatedObject) -> float:
        dLon = math.radians(obj.longitude - self.lon)
        y = math.sin(dLon) * math.cos(math.radians(obj.latitude))
        x = math.cos(math.radians(self.lat)) * math.sin(math.radians(obj.latitude)) - \\
            math.sin(math.radians(self.lat)) * math.cos(math.radians(obj.latitude)) * math.cos(dLon)
        bearing = math.atan2(y, x)
        bearing = math.degrees(bearing)
        return (bearing + 360) % 360
        
    def tick(self, objects: List[SimulatedObject], sim_time: datetime) -> List[Dict[str, Any]]:
        if self.random.random() < self.dropout_probability:
            return []
            
        payloads = []
        for obj in objects:
            dist = self._distance_m(obj)
            if dist <= self.coverage_radius_m:
                payload = self.generate_observation(obj, sim_time, dist)
                if payload:
                    payloads.append(payload)
        return payloads

    @abstractmethod
    def generate_observation(self, obj: SimulatedObject, sim_time: datetime, dist_m: float) -> Optional[Dict[str, Any]]:
        pass
""",

    "generators/radar.py": """from .base import SensorSimulator
from typing import Dict, Any, Optional
from datetime import datetime
from app.simulation.models import SimulatedObject

class RadarSimulator(SensorSimulator):
    def generate_observation(self, obj: SimulatedObject, sim_time: datetime, dist_m: float) -> Optional[Dict[str, Any]]:
        # Radar noise
        lat_noise = (self.random.random() - 0.5) * 0.0001
        lon_noise = (self.random.random() - 0.5) * 0.0001
        vel_noise = (self.random.random() - 0.5) * 1.0
        
        bearing = self._bearing_deg(obj)
        
        return {
            "range_m": dist_m,
            "azimuth_deg": bearing,
            "elevation_deg": 10.0,
            "radial_velocity_mps": max(0.0, obj.speed + vel_noise),
            "confidence": 0.9 + (self.random.random() * 0.1 - 0.05),
            "lat": obj.latitude + lat_noise,
            "lon": obj.longitude + lon_noise,
            "alt": obj.altitude
        }
""",

    "generators/rf.py": """from .base import SensorSimulator
from typing import Dict, Any, Optional
from datetime import datetime
from app.simulation.models import SimulatedObject

class RFSimulator(SensorSimulator):
    def generate_observation(self, obj: SimulatedObject, sim_time: datetime, dist_m: float) -> Optional[Dict[str, Any]]:
        # Only detect objects emitting RF
        if obj.metadata.get("rf_emitter", True) is False:
            return None
            
        bearing = self._bearing_deg(obj)
        bearing_noise = (self.random.random() - 0.5) * 2.0
        
        signal_dbm = -50 - (dist_m / 1000)
        
        return {
            "frequency_hz": 2400000000,
            "signal_strength_dbm": signal_dbm,
            "confidence": 0.7 + (self.random.random() * 0.2 - 0.1),
            "bearing": (bearing + bearing_noise) % 360,
            "lat": self.lat,
            "lon": self.lon
        }
""",

    "generators/eo_ir.py": """from .base import SensorSimulator
from typing import Dict, Any, Optional
from datetime import datetime
from app.simulation.models import SimulatedObject

class EOIRSimulator(SensorSimulator):
    def generate_observation(self, obj: SimulatedObject, sim_time: datetime, dist_m: float) -> Optional[Dict[str, Any]]:
        # Lower coverage for optical
        if dist_m > 5000:
            return None
            
        lat_noise = (self.random.random() - 0.5) * 0.00005
        lon_noise = (self.random.random() - 0.5) * 0.00005
        
        return {
            "latitude": obj.latitude + lat_noise,
            "longitude": obj.longitude + lon_noise,
            "altitude": obj.altitude,
            "confidence": 0.85 + (self.random.random() * 0.1)
        }
""",

    "generators/acoustic.py": """from .base import SensorSimulator
from typing import Dict, Any, Optional
from datetime import datetime
from app.simulation.models import SimulatedObject

class AcousticSimulator(SensorSimulator):
    def generate_observation(self, obj: SimulatedObject, sim_time: datetime, dist_m: float) -> Optional[Dict[str, Any]]:
        if dist_m > 3000:
            return None
            
        bearing = self._bearing_deg(obj)
        bearing_noise = (self.random.random() - 0.5) * 5.0
        
        return {
            "bearing_deg": (bearing + bearing_noise) % 360,
            "frequency_hz": 120 + (self.random.random() * 20),
            "confidence": 0.5 + (self.random.random() * 0.3),
            "lat": self.lat,
            "lon": self.lon
        }
""",

    "generators/__init__.py": """from .base import SensorSimulator
from .radar import RadarSimulator
from .rf import RFSimulator
from .eo_ir import EOIRSimulator
from .acoustic import AcousticSimulator
from app.simulation.registry import simulator_registry

simulator_registry.register("RADAR", RadarSimulator)
simulator_registry.register("RF", RFSimulator)
simulator_registry.register("EO_IR", EOIRSimulator)
simulator_registry.register("ACOUSTIC", AcousticSimulator)

__all__ = ["SensorSimulator"]
""",

    "scenarios.py": """from typing import List, Dict, Any, Tuple
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
""",

    "engine.py": """import random
import time
from datetime import datetime, timezone, timedelta
import threading
from typing import List, Optional
from app.simulation.models import SimulationConfig, SimulationStatus, SimulatedObject
from app.simulation.registry import simulator_registry
import app.simulation.generators # to load registry
from app.simulation.scenarios import SCENARIOS, SimulationScenario
from app.services.observations_service import observations_service
from app.infrastructure.db.session import SessionLocal

class SimulationEngine:
    def __init__(self):
        self.config = SimulationConfig()
        self.status = SimulationStatus()
        self.scenario: Optional[SimulationScenario] = None
        self.simulators = []
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self.random_gen = random.Random()
        self.sim_time: datetime = datetime.now(timezone.utc)

    def start(self, config: SimulationConfig):
        if self._thread and self._thread.is_alive():
            self.stop()
            
        self.config = config
        self.random_gen.seed(config.random_seed)
        
        scenario_cls = SCENARIOS.get(config.scenario)
        if not scenario_cls:
            raise ValueError(f"Unknown scenario: {config.scenario}")
            
        self.scenario = scenario_cls()
        self.scenario.setup()
        
        self.simulators = []
        for s in self.scenario.sensors:
            sim_cls = simulator_registry.get(s.sensor_type)
            simulator = sim_cls(s, self.random_gen)
            if getattr(self.scenario, "dropout_override", None) is not None:
                simulator.dropout_probability = self.scenario.dropout_override
            self.simulators.append(simulator)
            
        self.sim_time = datetime.now(timezone.utc)
        self.status.running = True
        self.status.scenario = config.scenario
        self.status.real_time_factor = config.speed
        self.status.active_objects = len(self.scenario.objects)
        self.status.active_sensors = len(self.simulators)
        self.status.observations_generated = 0
        self.status.observations_rejected = 0
        
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        
    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join()
        self.status.running = False
        
    def _run_loop(self):
        tick_s = self.config.tick_interval_ms / 1000.0
        
        while not self._stop_event.is_set():
            start_t = time.time()
            
            # Move objects
            dt_sim = tick_s * self.config.speed
            for obj in self.scenario.objects:
                obj.move(dt_sim)
                
            self.sim_time += timedelta(seconds=dt_sim)
            self.status.simulation_time = self.sim_time
            self.status.last_tick = datetime.now(timezone.utc)
            
            # Generate observations
            db = SessionLocal()
            for sim in self.simulators:
                try:
                    payloads = sim.tick(self.scenario.objects, self.sim_time)
                    for i, p in enumerate(payloads):
                        # Add a deterministic correlation ID based on seed, sim_time, sensor, object_index
                        corr_id = f"sim_{self.config.random_seed}_{self.sim_time.timestamp()}_{sim.id}_{i}"
                        
                        # Add latency
                        latency = self.random_gen.random() * 0.5
                        p["_sim_observed_at"] = self.sim_time
                        p["_sim_received_at"] = self.sim_time + timedelta(seconds=latency)
                        
                        try:
                            # We can't pass received_at through raw payload easily without modifying adapter, 
                            # but the adapter sets received_at to datetime.now(timezone.utc).
                            # We will just pass the payload, ObservationService will ingest it normally.
                            observations_service.ingest_raw(db, sim.id, p, correlation_id=corr_id)
                            self.status.observations_generated += 1
                        except Exception as e:
                            self.status.observations_rejected += 1
                            # log e
                except Exception as e:
                    pass # log error
                    
            db.close()
            
            elapsed = time.time() - start_t
            sleep_time = tick_s - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

""",
    "runtime.py": """from .engine import SimulationEngine

simulation_runtime = SimulationEngine()
"""
}

for name, content in files.items():
    path = os.path.join(base_dir, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

print("Simulation engine written.")
