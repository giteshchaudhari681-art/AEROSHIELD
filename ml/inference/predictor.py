import os
from pydantic import BaseModel
from ml.models.classifier import TrackClassifier

class PredictionRequest(BaseModel):
    speed_mps: float
    altitude_m: float
    rcs_m2: float

class PredictionResponse(BaseModel):
    classification: str

class MLPredictorService:
    def __init__(self):
        # Look for model artifact in environment or default path
        model_path = os.getenv("AEROSHIELD_MODEL_PATH", "ml/artifacts/rf_model.joblib")
        self.classifier = TrackClassifier(model_path)
        
    def predict(self, req: PredictionRequest) -> PredictionResponse:
        """
        Run inference against the loaded ML model or fall back to heuristics.
        """
        result = self.classifier.predict(req.speed_mps, req.altitude_m, req.rcs_m2)
        return PredictionResponse(classification=result)

# Singleton instance
predictor = MLPredictorService()
