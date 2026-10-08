# AEROSHIELD

**Infrastructure-Aware Airspace Security & Threat Intelligence Platform**

AEROSHIELD is an infrastructure-aware drone surveillance and threat-intelligence platform prototype designed to fuse heterogeneous aerial-sensor observations, understand drone identity and behaviour, estimate potential intent, predict threat trajectories, assess risk to specific critical infrastructure assets, and provide explainable real-time alerts and actionable insights to human security operators.

## Prototype Scope
This project is being developed as a software prototype of the intelligence and decision-support layer.
- **What is simulated:** Sensor telemetry (Radar, RF, EO/IR, Acoustic). Real hardware will eventually be represented through clean sensor-adapter interfaces.
- **What is NOT implemented yet:** The full sensor fusion, AI intent engine, behavior engine, and physical countermeasure integration.

**Important Note:** The software is designed to provide actionable intelligence (DETECT -> FUSE -> IDENTIFY -> UNDERSTAND -> PREDICT -> ASSESS -> EXPLAIN -> ALERT -> HUMAN DECISION). The human operator remains responsible for security decisions.

## Architecture & Technology Stack
- **Frontend:** React, TypeScript, Vite, Tailwind CSS, MapLibre GL, Recharts
- **Backend:** Python, FastAPI, Pydantic, WebSockets
- **Database:** PostgreSQL with PostGIS extension
- **Cache/Real-time:** Redis
- **Infrastructure:** Docker, Docker Compose

## Local Setup

### Requirements
- Docker and Docker Compose
- Node.js (for local frontend development)
- Python 3.11+ (for local backend development)

### Quickstart
1. Clone the repository.
2. Copy `.env.example` to `.env` and adjust the variables if needed.
3. Start the application using Docker Compose:
   ```bash
   docker compose up --build
   ```
4. Access the application:
   - Web UI: http://localhost:5173
   - API Docs: http://localhost:8000/docs
   - API Health: http://localhost:8000/api/v1/health

## Testing
- Backend tests are located in `apps/api/tests/`. Run them using `pytest`.
- Integration tests are located in `tests/integration/`.

## API Documentation
Once the API is running, access the OpenAPI documentation at http://localhost:8000/docs.

## Development Workflow
Please refer to the `docs/` folder for architectural decisions, domain models, and development guidelines.
