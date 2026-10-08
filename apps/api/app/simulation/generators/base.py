from abc import ABC, abstractmethod
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
        x = math.cos(math.radians(self.lat)) * math.sin(math.radians(obj.latitude)) - \
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
