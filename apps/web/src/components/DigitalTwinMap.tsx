import React, { useEffect, useRef, useState } from 'react';
import * as maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

interface DigitalTwinMapProps {
  site: any;
  assets: any[];
  zones: any[];
  selectedAssetId?: string | null;
}

export const DigitalTwinMap: React.FC<DigitalTwinMapProps> = ({ site, assets, zones, selectedAssetId }) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);

  useEffect(() => {
    if (map.current && selectedAssetId) {
      const selected = assets.find(a => a.id === selectedAssetId);
      if (selected && selected.location && selected.location.coordinates) {
        map.current.flyTo({
          center: selected.location.coordinates as [number, number],
          zoom: 17,
          essential: true
        });
      }
    }
  }, [selectedAssetId, assets]);

  const [mapLoaded, setMapLoaded] = useState(false);

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
      setMapLoaded(true);
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
    if (!map.current || !mapLoaded) return;

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

      // Interactions
      map.current.on('click', 'assets-circle', (e) => {
        if (!e.features || e.features.length === 0) return;
        const props = e.features[0].properties;
        new maplibregl.Popup()
          .setLngLat(e.lngLat)
          .setHTML(`<div class="text-slate-900 p-1"><strong>${props.name}</strong><br/>Status: ${props.status}</div>`)
          .addTo(map.current!);
      });

      map.current.on('mouseenter', 'assets-circle', () => {
        if (map.current) map.current.getCanvas().style.cursor = 'pointer';
      });
      
      map.current.on('mouseleave', 'assets-circle', () => {
        if (map.current) map.current.getCanvas().style.cursor = '';
      });
      
      map.current.on('click', 'zones-fill', (e) => {
        if (!e.features || e.features.length === 0) return;
        const props = e.features[0].properties;
        new maplibregl.Popup()
          .setLngLat(e.lngLat)
          .setHTML(`<div class="text-slate-900 p-1"><strong>${props.name}</strong><br/>Severity: ${props.severity}</div>`)
          .addTo(map.current!);
      });
    }

  }, [assets, zones, mapLoaded]);

  return (
    <div className="relative w-full h-full rounded-xl overflow-hidden border border-gray-700 shadow-xl">
      <div ref={mapContainer} className="absolute inset-0" />
      <div className="absolute top-4 left-4 bg-slate-900/80 backdrop-blur-md text-white p-5 rounded-xl shadow-[0_0_30px_rgba(0,0,0,0.5)] border border-slate-700/50 z-10">
        <h3 className="font-bold text-lg mb-1 text-blue-300">{site?.name || 'Loading...'}</h3>
        <p className="text-xs text-slate-400 uppercase tracking-widest font-semibold mb-4">Live Satellite Feed</p>
        <div className="flex gap-4 text-xs font-mono">
          <div className="flex items-center"><span className="inline-block w-2 h-2 rounded-full bg-emerald-500 mr-2 shadow-[0_0_8px_rgba(16,185,129,0.8)]"></span> Operational</div>
          <div className="flex items-center"><span className="inline-block w-2 h-2 rounded-full bg-yellow-500 mr-2 shadow-[0_0_8px_rgba(234,179,8,0.8)]"></span> Degraded</div>
          <div className="flex items-center"><span className="inline-block w-2 h-2 rounded-full bg-red-500 mr-2 shadow-[0_0_8px_rgba(239,68,68,0.8)]"></span> Offline</div>
        </div>
      </div>

      {/* Selected Asset Detailed Panel Overlay */}
      <div className={`absolute top-4 right-4 bottom-4 w-80 bg-slate-900/85 backdrop-blur-xl border border-blue-500/30 rounded-2xl p-6 shadow-[0_0_50px_rgba(37,99,235,0.15)] transition-all duration-500 transform ${selectedAssetId ? 'translate-x-0 opacity-100' : 'translate-x-[120%] opacity-0'} z-20 flex flex-col`}>
        {selectedAssetId && assets.find(a => a.id === selectedAssetId) && (() => {
          const asset = assets.find(a => a.id === selectedAssetId);
          return (
            <>
              <div className="flex justify-between items-start mb-6 border-b border-slate-800 pb-4">
                <div>
                  <h3 className="text-xl font-black text-white mb-1">{asset.name}</h3>
                  <span className="text-xs font-mono text-slate-400 capitalize">{asset.asset_type.replace('_', ' ')}</span>
                </div>
                <span className={`text-[10px] px-2 py-1 rounded font-black uppercase tracking-wider ${
                  asset.operational_status === 'OPERATIONAL' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' :
                  asset.operational_status === 'DEGRADED' ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30' :
                  'bg-red-500/20 text-red-400 border border-red-500/30'
                }`}>
                  {asset.operational_status}
                </span>
              </div>
              
              <div className="space-y-6 flex-1 overflow-y-auto custom-scrollbar pr-2">
                <div className="bg-slate-950/50 rounded-lg p-4 border border-slate-800/50">
                  <h4 className="text-[10px] text-blue-400 uppercase tracking-widest font-bold mb-2">Telemetry Data</h4>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <span className="block text-slate-500 text-xs mb-1">LATITUDE</span>
                      <span className="font-mono text-sm text-slate-200">{asset.location?.coordinates[1]?.toFixed(4)}°</span>
                    </div>
                    <div>
                      <span className="block text-slate-500 text-xs mb-1">LONGITUDE</span>
                      <span className="font-mono text-sm text-slate-200">{asset.location?.coordinates[0]?.toFixed(4)}°</span>
                    </div>
                  </div>
                </div>

                <div className="bg-slate-950/50 rounded-lg p-4 border border-slate-800/50">
                  <h4 className="text-[10px] text-blue-400 uppercase tracking-widest font-bold mb-2">Criticality Level</h4>
                  <div className="flex items-center gap-3">
                    <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
                      <div className={`h-full ${
                        asset.criticality === 'CRITICAL' ? 'w-full bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.8)]' :
                        asset.criticality === 'HIGH' ? 'w-3/4 bg-orange-500 shadow-[0_0_10px_rgba(249,115,22,0.8)]' :
                        'w-1/2 bg-yellow-500 shadow-[0_0_10px_rgba(234,179,8,0.8)]'
                      }`}></div>
                    </div>
                    <span className="font-bold text-xs uppercase text-slate-300">{asset.criticality}</span>
                  </div>
                </div>

                <div className="bg-slate-950/50 rounded-lg p-4 border border-slate-800/50">
                  <h4 className="text-[10px] text-blue-400 uppercase tracking-widest font-bold mb-2">System Logs</h4>
                  <div className="space-y-2 font-mono text-[10px]">
                    <div className="text-emerald-400">&gt; Connection established</div>
                    <div className="text-slate-400">&gt; Sensor array nominal</div>
                    <div className="text-slate-400">&gt; Data streaming active</div>
                    <div className="text-blue-400 animate-pulse">&gt; Monitoring...</div>
                  </div>
                </div>
              </div>
              
              <button className="mt-4 w-full bg-blue-600/20 hover:bg-blue-600/40 text-blue-400 border border-blue-500/50 rounded-lg py-3 font-bold text-sm transition-all hover:shadow-[0_0_15px_rgba(59,130,246,0.3)] flex items-center justify-center gap-2">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                View Live Camera Feed
              </button>
            </>
          );
        })()}
      </div>
    </div>
  );
};
