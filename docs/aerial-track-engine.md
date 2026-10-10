# Aerial Track Engine

AEROSHIELD's Aerial Track Engine associates fused contacts over time into continuous estimated `AerialTrack` entities.

## Pipeline Flow

1. **Trigger**: Driven by fused contacts.
2. **Persistence**: `AerialTrack` and `TrackObservation` tables in PostGIS.
3. **Logic**: Gating on temporal (ms) and spatial (m) windows. Association compares incoming fused contacts against existing active/tentative tracks. 
4. **Lifecycle**: TENTATIVE -> ACTIVE -> STALE -> TERMINATED.

## Configuration

Gates and weights are configurable via environment variables or `config.py`:
- `TRACK_ASSOCIATION_TIME_GATE_SECONDS`: Maximum time delta for tracks.
- `TRACK_ASSOCIATION_DISTANCE_GATE_METERS`: Maximum spatial distance.
- `TRACK_CONFIRMATION_HITS`: Required hits to move from TENTATIVE to ACTIVE.
- `TRACK_STALE_TIMEOUT_SECONDS`: Time before marking track stale.
- `TRACK_TERMINATION_TIMEOUT_SECONDS`: Time before track termination.
