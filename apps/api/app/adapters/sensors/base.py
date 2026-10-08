from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime, timezone
import uuid
from app.schemas.extended import ObservationBase
from app.infrastructure.db.models import ObservationType, SensorHealthStatus

class SensorAdapter(ABC):
    """
    Abstract base class for all sensor adapters.
    """
    
    @property
    @abstractmethod
    def sensor_type(self) -> str:
        """Returns the sensor type this adapter supports, e.g., 'RADAR'."""
        pass
        
    @abstractmethod
    def normalize(self, sensor_id: str, raw_payload: Dict[str, Any]) -> List[ObservationBase]:
        """
        Normalizes a raw sensor payload into one or more canonical AEROSHIELD observations.
        """
        pass
        
    def health(self) -> SensorHealthStatus:
        """
        Returns the synthetic health status of the adapter/sensor connection.
        """
        return SensorHealthStatus.HEALTHY

class AdapterRegistry:
    def __init__(self):
        self._adapters: Dict[str, SensorAdapter] = {}
        
    def register(self, adapter: SensorAdapter):
        self._adapters[adapter.sensor_type] = adapter
        
    def get(self, sensor_type: str) -> SensorAdapter:
        if sensor_type not in self._adapters:
            raise ValueError(f"No adapter registered for sensor type: {sensor_type}")
        return self._adapters[sensor_type]
        
    def list_supported_types(self) -> List[str]:
        return list(self._adapters.keys())

# Global registry instance
registry = AdapterRegistry()
