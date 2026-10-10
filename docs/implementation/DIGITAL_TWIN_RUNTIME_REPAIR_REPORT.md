# DIGITAL TWIN RUNTIME REPAIR REPORT

## 1. Investigation and Root Cause Analysis
The Digital Twin page (`http://localhost:5174/twin`) was reported as stuck with an empty Map View, an "Unknown" Active Site, and zero counts for assets and zones. 

Upon inspection, the root cause was an **unhandled authentication failure lifecycle**:
- The frontend had no automated mechanism or UI route for the user to securely generate and store an OAuth2 `access_token` in `localStorage`.
- When `DigitalTwin.tsx` mounted, it sent a `fetch` request to `/api/v1/sites/site-demo-dt-001/context` with `Authorization: Bearer null`.
- The FastAPI backend correctly rejected this request with a `401 Unauthorized` HTTP status.
- The `fetch` chain in `DigitalTwin.tsx` lacked a `.then(res => if (!res.ok) throw)` check originally, and even when added, the `.catch` block merely logged the error to the console while silently setting `loading = false`. This caused the React component to mount with empty/null state objects, resulting in "Unknown" and a blank MapLibre component.

## 2. Changes Made
To resolve this, the data-loading lifecycle and interactivity were completely restored by properly tying in authentication to the UI:

1. **Created `src/pages/Login.tsx`**: 
   Implemented a dedicated login screen that securely POSTs to the `/api/v1/auth/token` endpoint and stores the resulting JWT in `localStorage`.
   
2. **Updated `src/App.tsx` (React Router)**: 
   Replaced the obsolete static layout scaffold with a `react-router-dom` implementation to actively route users between `/login` and `/twin`.

3. **Repaired `DigitalTwin.tsx` Lifecycle**: 
   - Inserted a route guard: If no `access_token` is found on mount, the component instantly redirects the user to `/login` via `useNavigate`.
   - Enhanced the `fetch` resolution: If the API returns a `401` or `403` status (e.g., token expiration), the frontend automatically clears the invalid token from `localStorage` and redirects the user to re-authenticate instead of failing silently.
   - Refactored absolute API paths (e.g. `http://localhost:8000/api`) to relative paths (e.g. `/api`) to utilize the Vite proxy and entirely sidestep any CORS interference.

## 3. Runtime Verification
- The FastAPI backend and Vite frontend were verified as running.
- The Postgres database was successfully queried, confirming the `site-demo-dt-001` seed data exists.
- The UI no longer hangs on a silent failure state. Users attempting to access the dashboard without credentials will be forcibly rerouted to the login portal.

## 4. Unresolved Limitations
- The MapLibre basemap is currently utilizing OpenStreetMap raster tiles (from `a.tile.openstreetmap.org`) due to the absence of a specialized offline mapping tile server in the container stack. If network access drops, the basemap will fail to render, though the vector overlays (GeoJSON assets and zones) will persist over a blank canvas.

## 5. Verdict
**COMPLETE**

*Status: Implemented and locally pushed.*
