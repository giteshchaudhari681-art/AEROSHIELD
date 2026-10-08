import React, { useEffect, useRef, useState } from 'react';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

interface DigitalTwinMapProps {
  site: any;
  assets: any[];
  zones: any[];
}

export const DigitalTwinMap: React.FC<DigitalTwinMapProps> = ({ site, assets, zones }) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);

  useEffect(() => {
    if (map.current) return;
    if (!mapContainer.current) return;

    // Center on site or default to San Francisco
    const center = site?.location?.coordinates || [-122.4194, 37.7749];

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          osm: {
            type: 'raster',
            tiles: ["https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"],
            tileSize: 256,
          }
        },
        layers: [{
          id: 'osm',
          type: 'raster',
          source: 'osm',
          minzoom: 0,
          maxzoom: 22
        }]
      },
      center: center,
      zoom: 14
    });

    map.current.on('load', () => {
      // Add Site Boundary
      if (site && site.boundary) {
        map.current?.addSource('site-boundary', {
          type: 'geojson',
          data: { type: 'Feature', geometry: site.boundary, properties: {} }
        });
        map.current?.addLayer({
          id: 'site-boundary-fill',
          type: 'fill',
          source: 'site-boundary',
          paint: { 'fill-color': '#088', 'fill-opacity': 0.1 }
        });
        map.current?.addLayer({
          id: 'site-boundary-line',
          type: 'line',
          source: 'site-boundary',
          paint: { 'line-color': '#088', 'line-width': 2 }
        });
      }
    });
  }, [site]);

  useEffect(() => {
    if (!map.current || !map.current.isStyleLoaded()) return;

    // Update Zones
    const zoneFeatures = zones.filter(z => z.boundary).map(z => ({
      type: 'Feature',
      geometry: z.boundary,
      properties: { name: z.name, severity: z.severity }
    }));
    
    if (map.current.getSource('zones')) {
      (map.current.getSource('zones') as maplibregl.GeoJSONSource).setData({
        type: 'FeatureCollection',
        features: zoneFeatures
      });
    } else {
      map.current.addSource('zones', {
        type: 'geojson',
        data: { type: 'FeatureCollection', features: zoneFeatures }
      });
      map.current.addLayer({
        id: 'zones-fill',
        type: 'fill',
        source: 'zones',
        paint: {
          'fill-color': [
            'match', ['get', 'severity'],
            'CRITICAL', '#ef4444',
            'HIGH', '#f97316',
            'MEDIUM', '#eab308',
            'LOW', '#3b82f6',
            '#9ca3af'
          ],
          'fill-opacity': 0.3
        }
      });
    }

    // Update Assets
    const assetFeatures = assets.filter(a => a.location).map(a => ({
      type: 'Feature',
      geometry: a.location,
      properties: { name: a.name, criticality: a.criticality, status: a.operational_status }
    }));

    if (map.current.getSource('assets')) {
      (map.current.getSource('assets') as maplibregl.GeoJSONSource).setData({
        type: 'FeatureCollection',
        features: assetFeatures
      });
    } else {
      map.current.addSource('assets', {
        type: 'geojson',
        data: { type: 'FeatureCollection', features: assetFeatures }
      });
      map.current.addLayer({
        id: 'assets-circle',
        type: 'circle',
        source: 'assets',
        paint: {
          'circle-radius': 6,
          'circle-color': [
            'match', ['get', 'status'],
            'OPERATIONAL', '#22c55e',
            'DEGRADED', '#eab308',
            'MAINTENANCE', '#3b82f6',
            'OFFLINE', '#ef4444',
            '#9ca3af'
          ],
          'circle-stroke-color': '#fff',
          'circle-stroke-width': 2
        }
      });
    }

  }, [assets, zones]);

  return (
    <div className="relative w-full h-full rounded-xl overflow-hidden border border-gray-700 shadow-xl">
      <div ref={mapContainer} className="absolute inset-0" />
      <div className="absolute top-4 left-4 bg-slate-900/80 backdrop-blur text-white p-4 rounded-lg shadow-lg border border-slate-700">
        <h3 className="font-semibold text-lg mb-2">{site?.name || 'Loading...'}</h3>
        <p className="text-sm text-slate-300">Digital Twin Active</p>
        <div className="mt-4 flex gap-4 text-xs">
          <div><span className="inline-block w-3 h-3 rounded-full bg-green-500 mr-2"></span> Operational</div>
          <div><span className="inline-block w-3 h-3 rounded-full bg-yellow-500 mr-2"></span> Degraded</div>
          <div><span className="inline-block w-3 h-3 rounded-full bg-red-500 mr-2"></span> Offline</div>
        </div>
      </div>
    </div>
  );
};
