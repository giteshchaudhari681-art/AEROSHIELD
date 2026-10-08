import os

class FusionConfig:
    FUSION_TIME_WINDOW_MS = int(os.getenv("FUSION_TIME_WINDOW_MS", "2000"))
    FUSION_POSITION_GATE_METERS = float(os.getenv("FUSION_POSITION_GATE_METERS", "50.0"))
    FUSION_ALTITUDE_GATE_METERS = float(os.getenv("FUSION_ALTITUDE_GATE_METERS", "20.0"))
    FUSION_SPEED_GATE_MPS = float(os.getenv("FUSION_SPEED_GATE_MPS", "10.0"))
    
    FUSION_MIN_CONFIDENCE = float(os.getenv("FUSION_MIN_CONFIDENCE", "0.5"))
    FUSION_MAX_CANDIDATES = int(os.getenv("FUSION_MAX_CANDIDATES", "10"))
    
    W_TIME = 0.2
    W_DISTANCE = 0.4
    W_MEASUREMENT = 0.2
    W_SENSOR = 0.2

    @classmethod
    def validate(cls):
        if cls.FUSION_TIME_WINDOW_MS <= 0:
            raise ValueError("FUSION_TIME_WINDOW_MS must be > 0")
        if cls.FUSION_POSITION_GATE_METERS <= 0:
            raise ValueError("FUSION_POSITION_GATE_METERS must be > 0")
        if cls.FUSION_MIN_CONFIDENCE < 0 or cls.FUSION_MIN_CONFIDENCE > 1:
            raise ValueError("FUSION_MIN_CONFIDENCE must be between 0 and 1")

FusionConfig.validate()
