import joblib
import numpy as np

class TrackClassifier:
    def __init__(self, model_path: str = None):
        self.model = None
        if model_path:
            self.load(model_path)

    def load(self, path: str):
        try:
            self.model = joblib.load(path)
        except Exception as e:
            print(f"Failed to load model: {e}")
            self.model = None

    def predict(self, speed: float, altitude: float, rcs: float) -> str:
        """
        Predict track classification.
        Features: [speed_mps, altitude_m, rcs_m2]
        """
        if not self.model:
            # Fallback to heuristics if model is missing
            if speed > 15 and rcs < 0.05:
                return "DRONE"
            if speed < 15 and altitude < 100:
                return "BIRD"
            return "UNKNOWN"
            
        features = np.array([[speed, altitude, rcs]])
        prediction = self.model.predict(features)[0]
        return prediction
