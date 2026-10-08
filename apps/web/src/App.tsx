import { useState, useEffect } from 'react';
import { Shield, Activity, Radio, AlertTriangle } from 'lucide-react';

function App() {
  const [health, setHealth] = useState<any>(null);

  useEffect(() => {
    fetch('/api/v1/health')
      .then((res) => res.json())
      .then((data) => setHealth(data))
      .catch((err) => console.error('Error fetching health:', err));
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col">
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur p-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Shield className="w-8 h-8 text-blue-500" />
          <h1 className="text-xl font-bold tracking-wider">AEROSHIELD</h1>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 text-sm">
            <Activity className="w-4 h-4 text-emerald-500" />
            <span className={health?.status === 'ok' ? 'text-emerald-500' : 'text-slate-500'}>
              API: {health?.status || 'Unknown'}
            </span>
          </div>
        </div>
      </header>

      <main className="flex-1 p-6 grid grid-cols-12 gap-6">
        <div className="col-span-3 bg-slate-800/50 border border-slate-700 rounded-xl p-4">
          <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">Sensors</h2>
          <ul className="space-y-3">
            <li className="flex items-center gap-3">
              <div className="p-2 bg-blue-500/10 rounded-lg">
                <Radio className="w-4 h-4 text-blue-500" />
              </div>
              <span className="text-sm font-medium">Radar Alpha</span>
              <span className="ml-auto flex w-2 h-2 rounded-full bg-emerald-500"></span>
            </li>
            <li className="flex items-center gap-3">
              <div className="p-2 bg-blue-500/10 rounded-lg">
                <Radio className="w-4 h-4 text-blue-500" />
              </div>
              <span className="text-sm font-medium">RF Scanner 1</span>
              <span className="ml-auto flex w-2 h-2 rounded-full bg-emerald-500"></span>
            </li>
          </ul>
        </div>
        
        <div className="col-span-6 bg-slate-800/50 border border-slate-700 rounded-xl p-4 flex items-center justify-center">
          <div className="text-center text-slate-500">
            <Shield className="w-16 h-16 mx-auto mb-4 opacity-20" />
            <p>Map View Placeholder</p>
          </div>
        </div>

        <div className="col-span-3 bg-slate-800/50 border border-slate-700 rounded-xl p-4">
          <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">Alerts</h2>
          <ul className="space-y-3">
            <li className="flex items-start gap-3 bg-slate-800 p-3 rounded-lg border border-slate-700">
              <AlertTriangle className="w-5 h-5 text-amber-500 shrink-0" />
              <div>
                <p className="text-sm font-medium text-amber-500">Unidentified Track</p>
                <p className="text-xs text-slate-400 mt-1">Zone C - Possible drone activity</p>
              </div>
            </li>
          </ul>
        </div>
      </main>
    </div>
  );
}

export default App;
