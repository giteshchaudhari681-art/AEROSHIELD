import random
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
from sqlalchemy import func

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
        
        db = SessionLocal()
        self.simulators = []
        for s in self.scenario.sensors:
            sim_cls = simulator_registry.get(s.sensor_type)
            simulator = sim_cls(s, self.random_gen)
            
            # Fetch coordinates
            from app.infrastructure.db.models import Sensor
            coords = db.query(func.ST_X(Sensor.location), func.ST_Y(Sensor.location)).filter(Sensor.id == s.id).first()
            if coords:
                simulator.lon = coords[0]
                simulator.lat = coords[1]
                
            if getattr(self.scenario, "dropout_override", None) is not None:
                simulator.dropout_probability = self.scenario.dropout_override
            self.simulators.append(simulator)
        db.close()
            
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
                        p["_sim_observed_at"] = self.sim_time.isoformat()
                        p["_sim_received_at"] = (self.sim_time + timedelta(seconds=latency)).isoformat()
                        
                        try:
                            # We can't pass received_at through raw payload easily without modifying adapter, 
                            # but the adapter sets received_at to datetime.now(timezone.utc).
                            # We will just pass the payload, ObservationService will ingest it normally.
                            observations_service.ingest_raw(db, sim.id, p, correlation_id=corr_id)
                            self.status.observations_generated += 1
                        except Exception as e:
                            self.status.observations_rejected += 1
                            import traceback
                            traceback.print_exc()
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    
            db.close()
            
            elapsed = time.time() - start_t
            sleep_time = tick_s - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

