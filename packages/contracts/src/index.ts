export interface Observation {
  observation_id: string;
  sensor_id: string;
  timestamp: string;
  location: {
    type: "Point";
    coordinates: [number, number];
  };
  altitude_m: number;
  speed_mps: number;
  heading: number;
  rcs_m2?: number;
  snr_db?: number;
}

export interface FusedContact {
  fused_contact_id: string;
  site_id: string;
  reference_time: string;
  location: any;
  altitude_m: number;
  speed_mps: number;
  heading: number;
  confidence: number;
  status: "ACTIVE" | "STALE" | "DROPPED";
}
