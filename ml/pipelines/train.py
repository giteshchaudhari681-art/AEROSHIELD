import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def generate_synthetic_data(num_samples: int = 1000):
    """
    Generate synthetic data for training the classifier.
    Features: [speed_mps, altitude_m, rcs_m2]
    """
    X = []
    y = []
    
    for _ in range(num_samples):
        is_drone = np.random.rand() > 0.5
        if is_drone:
            # Drones: moderate speed, medium altitude, small RCS
            speed = np.random.uniform(10, 30)
            alt = np.random.uniform(20, 200)
            rcs = np.random.uniform(0.01, 0.05)
            X.append([speed, alt, rcs])
            y.append("DRONE")
        else:
            # Birds: low speed, low altitude, very small RCS
            speed = np.random.uniform(2, 12)
            alt = np.random.uniform(5, 50)
            rcs = np.random.uniform(0.001, 0.01)
            X.append([speed, alt, rcs])
            y.append("BIRD")
            
    return np.array(X), np.array(y)

def train_pipeline(model_output_dir: str = "ml/artifacts"):
    print("Generating synthetic training data...")
    X_train, y_train = generate_synthetic_data(1000)
    
    print("Training RandomForest model...")
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X_train, y_train)
    
    score = clf.score(X_train, y_train)
    print(f"Training completed. Internal accuracy score: {score:.2f}")
    
    os.makedirs(model_output_dir, exist_ok=True)
    model_path = os.path.join(model_output_dir, "rf_model.joblib")
    joblib.dump(clf, model_path)
    print(f"Model successfully saved to {model_path}")

if __name__ == "__main__":
    train_pipeline()
