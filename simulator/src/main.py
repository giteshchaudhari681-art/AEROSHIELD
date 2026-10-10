import time
import json
import random
import requests
from datetime import datetime, timezone

API_URL = "http://localhost:8000/api/v1/sensors/observations"

def generate_observation(sensor_id="sim-radar-01"):
    return {
        "sensor_id": sensor_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "location": {
            "type": "Point",
            "coordinates": [-122.4194 + random.uniform(-0.01, 0.01), 37.7749 + random.uniform(-0.01, 0.01)]
        },
        "altitude_m": random.uniform(50, 500),
        "speed_mps": random.uniform(0, 30),
        "heading": random.uniform(0, 360),
        "rcs_m2": random.uniform(0.01, 0.1),
        "snr_db": random.uniform(10, 30)
    }

def run_simulation(token: str, duration_sec: int = 60, interval_sec: float = 1.0):
    print(f"Starting simulation for {duration_sec} seconds...")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    start_time = time.time()
    count = 0
    while time.time() - start_time < duration_sec:
        obs = generate_observation()
        try:
            resp = requests.post(API_URL, json=obs, headers=headers)
            if resp.status_code == 200:
                print(f"[{datetime.now().isoformat()}] Sent observation: {resp.json().get('observation_id')}")
                count += 1
            else:
                print(f"Error: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"Connection error: {e}")
            
        time.sleep(interval_sec)
    print(f"Simulation complete. Sent {count} observations.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <jwt_token>")
        sys.exit(1)
    
    token = sys.argv[1]
    run_simulation(token)
