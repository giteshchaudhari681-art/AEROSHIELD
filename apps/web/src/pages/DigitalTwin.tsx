import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { DigitalTwinMap } from '../components/DigitalTwinMap';

export const DigitalTwin: React.FC = () => {
  const [site, setSite] = useState<any>(null);
  const [assets, setAssets] = useState<any[]>([]);
  const [zones, setZones] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedAssetId, setSelectedAssetId] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      navigate('/login');
      return;
    }
    
    fetch('/api/v1/sites/site-demo-dt-001/context', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        if (!res.ok) {
           if (res.status === 401 || res.status === 403) {
             localStorage.removeItem('access_token');
             navigate('/login');
           }
           throw new Error(`HTTP ${res.status}`);
        }
        return res.json();
      })
      .then(data => {
        if (data && data.site) {
          setSite(data.site);
          setAssets(data.assets || []);
          setZones(data.restricted_zones || []);
        }
      })
      .catch(err => {
        console.error("Failed to load Digital Twin:", err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [navigate]);

  if (loading) {
    return <div className="flex h-screen items-center justify-center bg-slate-950 text-white">Loading Digital Twin...</div>;
  }

  return (
    <div className="flex flex-col h-screen bg-slate-950 text-slate-100 font-sans relative overflow-hidden">
      {/* Background grid */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#1e293b_1px,transparent_1px),linear-gradient(to_bottom,#1e293b_1px,transparent_1px)] bg-[size:4rem_4rem] opacity-20 pointer-events-none z-0"></div>

      <header className="px-6 py-4 border-b border-slate-800/80 bg-slate-900/70 backdrop-blur-xl flex justify-between items-center relative z-10 shadow-lg">
        <div className="flex items-center gap-4">
          <div>
            <h1 className="text-2xl font-black tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">
              AEROSHIELD
            </h1>
            <p className="text-[10px] text-blue-500/80 font-bold uppercase tracking-[0.2em] mt-0.5">Live Digital Twin</p>
          </div>
        </div>
        <div className="flex gap-4">
          <div className="bg-slate-950/50 rounded-lg px-4 py-2 border border-slate-800 shadow-inner flex flex-col justify-center">
            <span className="text-[10px] text-slate-500 uppercase tracking-wider font-bold mb-0.5">Active Site</span>
            <span className="font-bold text-sm text-slate-200">{site?.name || 'Unknown'}</span>
          </div>
          <div className="bg-slate-950/50 rounded-lg px-4 py-2 border border-slate-800 shadow-inner flex flex-col justify-center">
            <span className="text-[10px] text-slate-500 uppercase tracking-wider font-bold mb-0.5">Critical Assets</span>
            <span className="font-bold text-sm text-blue-400 flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.8)]"></span>
              {assets.length}
            </span>
          </div>
          <div className="bg-slate-950/50 rounded-lg px-4 py-2 border border-slate-800 shadow-inner flex flex-col justify-center">
            <span className="text-[10px] text-slate-500 uppercase tracking-wider font-bold mb-0.5">Restricted Zones</span>
            <span className="font-bold text-sm text-yellow-400 flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-yellow-500 shadow-[0_0_8px_rgba(234,179,8,0.8)]"></span>
              {zones.length}
            </span>
          </div>
        </div>
      </header>

      <main className="flex-1 flex overflow-hidden p-6 gap-6 relative z-10">
        <div className="w-80 flex flex-col gap-6 overflow-y-auto pr-2 custom-scrollbar">
          
          {/* Site Info */}
          <section className="bg-slate-900/60 backdrop-blur-md rounded-xl p-5 border border-slate-800 shadow-xl relative overflow-hidden group">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <h2 className="text-sm font-bold uppercase tracking-wider mb-4 text-blue-400 flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              Site Context
            </h2>
            <div className="space-y-4 text-sm relative z-10">
              <div className="bg-slate-950/50 p-3 rounded-lg border border-slate-800/50">
                <span className="text-slate-500 text-xs font-bold uppercase tracking-wider block mb-1">Site Code</span>
                <span className="font-mono text-blue-300 font-semibold tracking-wider">{site?.site_code}</span>
              </div>
              <div className="bg-slate-950/50 p-3 rounded-lg border border-slate-800/50">
                <span className="text-slate-500 text-xs font-bold uppercase tracking-wider block mb-1">Type</span>
                <span className="text-slate-200 capitalize">{site?.site_type?.replace('_', ' ').toLowerCase()}</span>
              </div>
              <div className="bg-slate-950/50 p-3 rounded-lg border border-slate-800/50">
                <span className="text-slate-500 text-xs font-bold uppercase tracking-wider block mb-1">Description</span>
                <span className="text-slate-400 leading-relaxed text-xs">{site?.description}</span>
              </div>
            </div>
          </section>

          {/* Critical Assets List */}
          <section className="bg-slate-900/60 backdrop-blur-md rounded-xl p-5 border border-slate-800 shadow-xl flex-1 min-h-[300px] flex flex-col">
            <h2 className="text-sm font-bold uppercase tracking-wider mb-4 text-emerald-400 flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
              Critical Assets
            </h2>
            <div className="space-y-3 overflow-y-auto pr-1 flex-1 custom-scrollbar">
              {assets.map(a => (
                <div 
                  key={a.id} 
                  onClick={() => setSelectedAssetId(a.id)}
                  className={`p-4 rounded-xl border transition-all duration-300 cursor-pointer relative overflow-hidden ${
                    selectedAssetId === a.id 
                      ? 'bg-blue-900/20 border-blue-500/50 ring-1 ring-blue-500/50 shadow-[0_0_20px_rgba(59,130,246,0.15)]' 
                      : 'bg-slate-950/50 border-slate-800/80 hover:bg-slate-800 hover:border-slate-700'
                  }`}
                >
                  {selectedAssetId === a.id && (
                     <div className="absolute left-0 top-0 bottom-0 w-1 bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,1)]"></div>
                  )}
                  <div className="flex justify-between items-start mb-3">
                    <h3 className={`font-bold ${selectedAssetId === a.id ? 'text-blue-300' : 'text-slate-200'}`}>{a.name}</h3>
                    <span className={`text-[9px] px-2 py-1 rounded font-black uppercase tracking-wider ${
                      a.criticality === 'CRITICAL' ? 'bg-red-500/20 text-red-400 border border-red-500/30 shadow-[0_0_10px_rgba(239,68,68,0.2)]' :
                      a.criticality === 'HIGH' ? 'bg-orange-500/20 text-orange-400 border border-orange-500/30' :
                      a.criticality === 'MEDIUM' ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30' :
                      'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                    }`}>
                      {a.criticality}
                    </span>
                  </div>
                  <div className="flex justify-between items-center text-xs text-slate-400">
                    <span className="capitalize px-2 py-1 bg-slate-900 rounded border border-slate-800">{a.asset_type.replace('_', ' ').toLowerCase()}</span>
                    <span className={`flex items-center gap-1.5 font-semibold text-[10px] uppercase tracking-wider ${
                      a.operational_status === 'OPERATIONAL' ? 'text-emerald-400' :
                      a.operational_status === 'DEGRADED' ? 'text-yellow-400' :
                      a.operational_status === 'OFFLINE' ? 'text-red-400' :
                      'text-blue-400'
                    }`}>
                      <span className={`w-2 h-2 rounded-full bg-current ${a.operational_status === 'OPERATIONAL' ? 'animate-pulse shadow-[0_0_8px_rgba(52,211,153,0.8)]' : ''}`}></span>
                      {a.operational_status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </section>

        </div>

        {/* Map Section */}
        <section className="flex-1 rounded-2xl overflow-hidden bg-slate-900 border border-slate-800 shadow-[0_0_50px_rgba(0,0,0,0.5)] relative">
           <div className="absolute inset-0 border border-blue-500/10 rounded-2xl pointer-events-none z-20"></div>
           <DigitalTwinMap site={site} assets={assets} zones={zones} selectedAssetId={selectedAssetId} />
        </section>
      </main>
    </div>
  );
};
