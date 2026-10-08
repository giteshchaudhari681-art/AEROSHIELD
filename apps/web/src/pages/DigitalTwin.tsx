import React, { useEffect, useState } from 'react';
import { DigitalTwinMap } from '../components/DigitalTwinMap';

export const DigitalTwin: React.FC = () => {
  const [site, setSite] = useState<any>(null);
  const [assets, setAssets] = useState<any[]>([]);
  const [zones, setZones] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // We would normally fetch this from our API using the auth token.
    // Assuming token is in localStorage if auth is implemented in frontend.
    const token = localStorage.getItem('access_token');
    
    // Fetch context for our seed site
    fetch('http://localhost:8000/api/v1/sites/site-demo-dt-001/context', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => res.json())
      .then(data => {
        if (data && data.site) {
          setSite(data.site);
          setAssets(data.assets || []);
          setZones(data.restricted_zones || []);
        }
      })
      .catch(err => console.error("Failed to load Digital Twin:", err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="flex h-screen items-center justify-center bg-slate-950 text-white">Loading Digital Twin...</div>;
  }

  return (
    <div className="flex flex-col h-screen bg-slate-950 text-slate-100 font-sans">
      <header className="px-6 py-4 border-b border-slate-800 bg-slate-900/50 backdrop-blur flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-300">
            AEROSHIELD
          </h1>
          <p className="text-xs text-slate-400 uppercase tracking-widest mt-1">Infrastructure Digital Twin</p>
        </div>
        <div className="flex gap-4">
          <div className="bg-slate-800 rounded-lg px-4 py-2 border border-slate-700">
            <span className="text-xs text-slate-400 block mb-1">Active Site</span>
            <span className="font-semibold">{site?.name || 'Unknown'}</span>
          </div>
          <div className="bg-slate-800 rounded-lg px-4 py-2 border border-slate-700">
            <span className="text-xs text-slate-400 block mb-1">Critical Assets</span>
            <span className="font-semibold text-blue-400">{assets.length}</span>
          </div>
          <div className="bg-slate-800 rounded-lg px-4 py-2 border border-slate-700">
            <span className="text-xs text-slate-400 block mb-1">Restricted Zones</span>
            <span className="font-semibold text-yellow-400">{zones.length}</span>
          </div>
        </div>
      </header>

      <main className="flex-1 flex overflow-hidden p-6 gap-6">
        <div className="w-80 flex flex-col gap-6 overflow-y-auto pr-2 custom-scrollbar">
          
          {/* Site Info */}
          <section className="bg-slate-900 rounded-xl p-5 border border-slate-800 shadow-xl">
            <h2 className="text-lg font-semibold mb-4 text-blue-300 border-b border-slate-800 pb-2">Site Context</h2>
            <div className="space-y-3 text-sm">
              <div>
                <span className="text-slate-500 block">Site Code</span>
                <span className="font-mono">{site?.site_code}</span>
              </div>
              <div>
                <span className="text-slate-500 block">Type</span>
                <span>{site?.site_type?.replace('_', ' ')}</span>
              </div>
              <div>
                <span className="text-slate-500 block">Description</span>
                <span className="text-slate-300">{site?.description}</span>
              </div>
            </div>
          </section>

          {/* Critical Assets List */}
          <section className="bg-slate-900 rounded-xl p-5 border border-slate-800 shadow-xl flex-1 min-h-[300px]">
            <h2 className="text-lg font-semibold mb-4 text-emerald-300 border-b border-slate-800 pb-2">Critical Assets</h2>
            <div className="space-y-3">
              {assets.map(a => (
                <div key={a.id} className="p-3 bg-slate-800/50 rounded-lg border border-slate-700/50 hover:bg-slate-800 transition-colors">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-medium text-slate-200">{a.name}</h3>
                    <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase ${
                      a.criticality === 'CRITICAL' ? 'bg-red-500/20 text-red-400 border border-red-500/30' :
                      a.criticality === 'HIGH' ? 'bg-orange-500/20 text-orange-400 border border-orange-500/30' :
                      a.criticality === 'MEDIUM' ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30' :
                      'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                    }`}>
                      {a.criticality}
                    </span>
                  </div>
                  <div className="flex justify-between text-xs text-slate-400">
                    <span>{a.asset_type.replace('_', ' ')}</span>
                    <span className={`flex items-center gap-1.5 ${
                      a.operational_status === 'OPERATIONAL' ? 'text-green-400' :
                      a.operational_status === 'DEGRADED' ? 'text-yellow-400' :
                      a.operational_status === 'OFFLINE' ? 'text-red-400' :
                      'text-blue-400'
                    }`}>
                      <span className="w-1.5 h-1.5 rounded-full bg-current"></span>
                      {a.operational_status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </section>

        </div>

        {/* Map Section */}
        <section className="flex-1 rounded-xl overflow-hidden bg-slate-900 border border-slate-800 shadow-2xl relative">
           <DigitalTwinMap site={site} assets={assets} zones={zones} />
        </section>
      </main>
    </div>
  );
};
