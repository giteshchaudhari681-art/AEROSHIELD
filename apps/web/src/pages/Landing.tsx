import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, ChevronRight, Activity, Crosshair, Map, ShieldAlert, Cpu, Zap, Cloud, Database, Lock, CheckCircle, Navigation, Server, Search, Check, Layers, Radio } from 'lucide-react';
import { DigitalTwinMap } from '../components/DigitalTwinMap';

export const Landing: React.FC = () => {
  const navigate = useNavigate();
  const [scrolled, setScrolled] = useState(false);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    const handleMouseMove = (e: MouseEvent) => {
      setMousePos({ 
        x: (e.clientX / window.innerWidth) - 0.5, 
        y: (e.clientY / window.innerHeight) - 0.5 
      });
    };
    window.addEventListener('scroll', handleScroll);
    window.addEventListener('mousemove', handleMouseMove);
    return () => {
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  // Fake demo data for the landing page live map
  const demoSite = {
    id: "landing-site",
    name: "Golden Gate Sector",
    location: { type: "Point", coordinates: [-122.4783, 37.8199] },
    boundary: null
  };
  const demoAssets = [
    { id: "a1", name: "Unknown Drone", criticality: "HIGH", operational_status: "OFFLINE", location: { type: "Point", coordinates: [-122.475, 37.821] } },
    { id: "a2", name: "Auth Quadcopter", criticality: "LOW", operational_status: "OPERATIONAL", location: { type: "Point", coordinates: [-122.482, 37.818] } },
  ];
  const demoZones = [
    { id: "z1", name: "Restricted Airspace R-99", severity: "CRITICAL", boundary: { type: "Polygon", coordinates: [[[-122.48, 37.822], [-122.47, 37.822], [-122.47, 37.818], [-122.48, 37.818], [-122.48, 37.822]]] } }
  ];

  return (
    <div className="bg-slate-950 min-h-screen text-slate-200 font-sans selection:bg-blue-500/30 selection:text-blue-200 overflow-x-hidden perspective-[2000px]">
      
      {/* SECTION A - Navigation */}
      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 border-b ${scrolled ? 'bg-slate-950/80 backdrop-blur-md border-slate-800 shadow-lg' : 'bg-transparent border-transparent'}`}>
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-2 cursor-pointer" onClick={() => navigate('/')}>
            <Shield className="w-8 h-8 text-blue-500" />
            <span className="text-xl font-bold tracking-wide text-white">AEROSHIELD</span>
          </div>
          
          <div className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-300">
            <a href="#" className="text-blue-400">Home</a>
            <a href="#features" className="hover:text-white transition-colors">Features</a>
            <a href="#digital-twin" className="hover:text-white transition-colors">Digital Twin</a>
            <a href="#use-cases" className="hover:text-white transition-colors">Use Cases</a>
            <a href="#technology" className="hover:text-white transition-colors">Technology</a>
          </div>

          <div className="flex items-center gap-4">
            <button onClick={() => navigate('/login')} className="hidden sm:block text-sm font-medium text-slate-300 hover:text-white transition-colors">Sign In</button>
            <button onClick={() => navigate('/login')} className="bg-blue-600 hover:bg-blue-500 text-white px-5 py-2 rounded-lg text-sm font-semibold transition-all shadow-[0_0_15px_rgba(37,99,235,0.4)] hover:shadow-[0_0_25px_rgba(37,99,235,0.6)]">
              Get Started
            </button>
          </div>
        </div>
      </nav>

      {/* SECTION B - Cinematic Hero */}
      <section className="relative pt-32 pb-20 md:pt-48 md:pb-32 overflow-hidden flex items-center min-h-[90vh]">
        {/* Advanced 3D Parallax Background */}
        <div 
          className="absolute inset-0 z-0 transition-transform duration-200 ease-out bg-slate-950"
          style={{ transform: `translate3d(${mousePos.x * -30}px, ${mousePos.y * -30}px, 0) scale(1.05)` }}
        >
          <div className="absolute inset-0 bg-gradient-to-r from-slate-950 via-slate-950/90 to-slate-900/60 z-10"></div>
          <div className="absolute inset-0 bg-[url('/images/real_hero_1791617984377.jpg')] bg-cover bg-center opacity-30 z-0 mix-blend-luminosity shadow-inner blur-[1px]"></div>
          
          {/* Grid matrix pattern */}
          <div className="absolute inset-0 bg-[linear-gradient(to_right,#1e293b_1px,transparent_1px),linear-gradient(to_bottom,#1e293b_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_80%_60%_at_60%_40%,#000_70%,transparent_100%)] opacity-30 z-10 shadow-inner pointer-events-none"></div>
          
          {/* Glowing orbs for depth */}
          <div className="absolute top-1/4 right-1/4 w-[40rem] h-[40rem] bg-blue-600/10 rounded-full blur-[100px] pointer-events-none mix-blend-screen"></div>
          <div className="absolute bottom-1/4 right-1/3 w-[30rem] h-[30rem] bg-cyan-500/10 rounded-full blur-[80px] pointer-events-none mix-blend-screen"></div>
          <div className="absolute top-1/3 right-1/10 w-[20rem] h-[20rem] bg-violet-500/10 rounded-full blur-[60px] pointer-events-none mix-blend-screen"></div>
        </div>

        <div className="max-w-7xl mx-auto px-6 relative z-20 w-full flex flex-col lg:flex-row items-center gap-12">
          
          {/* Left Text */}
          <div 
            className="lg:w-1/2 flex flex-col items-start transition-transform duration-200"
            style={{ transform: `translate3d(${mousePos.x * 10}px, ${mousePos.y * 10}px, 0)` }}
          >
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-900/30 border border-blue-500/30 text-blue-400 text-xs font-bold uppercase tracking-widest mb-6 backdrop-blur-sm animate-fade-in-up shadow-[0_0_10px_rgba(37,99,235,0.2)]">
              <Activity className="w-3.5 h-3.5" /> AI-Powered Airspace Security
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold leading-tight mb-6 animate-fade-in-up animation-delay-100 drop-shadow-2xl">
              Turn a Single<br />Drone Video<br />
              Into a <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-cyan-300 to-emerald-300 drop-shadow-lg">Real 3D World</span>
            </h1>
            
            <p className="text-lg text-slate-300 mb-8 max-w-xl animate-fade-in-up animation-delay-200">
              AEROSHIELD transforms multi-sensor data into a live, spatially accurate 3D digital twin, detecting, tracking, and neutralizing unauthorized drone threats across critical infrastructure.
            </p>
            
            <div className="flex flex-wrap items-center gap-4 mb-12 animate-fade-in-up animation-delay-300">
              <button onClick={() => navigate('/login')} className="group flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white px-6 py-3 rounded-lg font-semibold transition-all shadow-[0_0_20px_rgba(37,99,235,0.5)] hover:shadow-[0_0_35px_rgba(37,99,235,0.7)] hover:-translate-y-1">
                Watch Live Demo <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </button>
              <button className="flex items-center gap-2 bg-slate-800/80 hover:bg-slate-700 backdrop-blur-md border border-slate-700 text-white px-6 py-3 rounded-lg font-semibold transition-all hover:-translate-y-1">
                Explore Features
              </button>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 w-full border-t border-slate-800/80 pt-8 animate-fade-in-up animation-delay-400">
              <div>
                <div className="text-2xl font-bold text-white flex items-center gap-2">
                  <ShieldAlert className="w-5 h-5 text-blue-500" /> 24/7
                </div>
                <div className="text-xs text-slate-400 mt-1 uppercase tracking-wider">Monitoring</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-white flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-cyan-400" /> 99.9%
                </div>
                <div className="text-xs text-slate-400 mt-1 uppercase tracking-wider">Uptime</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-white flex items-center gap-2">
                  <Zap className="w-5 h-5 text-emerald-400" /> &lt;1s
                </div>
                <div className="text-xs text-slate-400 mt-1 uppercase tracking-wider">Real-Time</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-white flex items-center gap-2">
                  <Layers className="w-5 h-5 text-violet-400" /> 3D
                </div>
                <div className="text-xs text-slate-400 mt-1 uppercase tracking-wider">Twin Maps</div>
              </div>
            </div>
          </div>

          {/* Right Visual Dashboard Mock with 3D Tilt */}
          <div className="lg:w-1/2 w-full relative animate-fade-in-up animation-delay-500 group perspective-[1000px] z-30 hidden md:block">
            <div 
              className="relative rounded-2xl overflow-hidden border border-slate-700/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.8),0_0_30px_rgba(6,182,212,0.15)] bg-slate-900/95 backdrop-blur-xl transition-transform duration-300 ease-out"
              style={{ transform: `rotateY(${mousePos.x * -15}deg) rotateX(${mousePos.y * 15}deg) scale(1.05)` }}
            >
              {/* Fake UI Header */}
              <div className="h-10 bg-slate-950/80 border-b border-slate-800/80 flex items-center px-4 gap-2 backdrop-blur">
                <div className="w-3 h-3 rounded-full bg-red-500/80 shadow-[0_0_10px_rgba(239,68,68,0.8)]"></div>
                <div className="w-3 h-3 rounded-full bg-yellow-500/80 shadow-[0_0_10px_rgba(234,179,8,0.8)]"></div>
                <div className="w-3 h-3 rounded-full bg-green-500/80 shadow-[0_0_10px_rgba(34,197,94,0.8)]"></div>
                <div className="ml-4 text-xs font-mono text-slate-400 flex-1 text-center tracking-widest">AEROSHIELD / LIVE_TRACK</div>
              </div>
              
              {/* ACTUAL LIVE 3D MAP in Hero (Satellite at night) */}
              <div className="relative h-[450px] w-full pointer-events-none bg-slate-950 overflow-hidden">
                 <img src="https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&q=80" alt="Satellite Map view" className="w-full h-full object-cover opacity-80 mix-blend-screen hue-rotate-180 brightness-125 contrast-125" />
                 <div className="absolute inset-0 bg-blue-900/30 mix-blend-overlay pointer-events-none"></div>
                 
                {/* Simulated Floating Overlays with Z-Translation for 3D depth */}
                <div 
                  className="absolute top-8 left-8 bg-slate-900/90 backdrop-blur-md border border-red-500/40 rounded-lg p-4 shadow-[0_10px_30px_rgba(239,68,68,0.2)] transition-transform duration-300"
                  style={{ transform: `translateZ(40px) translate3d(${mousePos.x * -20}px, ${mousePos.y * -20}px, 0)` }}
                >
                  <div className="flex items-center gap-2 text-red-400 font-bold text-xs mb-2 uppercase tracking-wider">
                    <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse shadow-[0_0_10px_rgba(239,68,68,1)]"></span> Threat Detected
                  </div>
                  <div className="grid grid-cols-2 gap-x-6 gap-y-1 text-sm">
                    <span className="text-slate-400">Type</span> <span className="text-white">UAV Class II</span>
                    <span className="text-slate-400">Speed</span> <span className="text-white">62 km/h</span>
                    <span className="text-slate-400">Risk</span> <span className="text-red-400 font-medium">CRITICAL</span>
                  </div>
                </div>

                {/* Simulated Zone Overlay */}
                <div 
                  className="absolute bottom-12 right-8 bg-slate-900/90 backdrop-blur-md border border-cyan-500/40 rounded-lg p-3 shadow-[0_10px_30px_rgba(6,182,212,0.1)] transition-transform duration-300"
                  style={{ transform: `translateZ(30px) translate3d(${mousePos.x * -10}px, ${mousePos.y * -10}px, 0)` }}
                >
                   <div className="text-cyan-400 text-xs font-semibold mb-1 flex items-center gap-2">
                     <Radio className="w-3 h-3" /> RF Sensor Online
                   </div>
                   <div className="text-slate-400 text-[10px]">Freq: 2.4GHz / Sector 9</div>
                </div>
              </div>
            </div>
          </div>
          
        </div>
      </section>

      {/* SECTION C - Capabilities */}
      <section id="features" className="py-24 bg-slate-950 relative z-10 border-t border-slate-900 shadow-[0_-20px_50px_rgba(0,0,0,0.5)]">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16 relative">
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-32 h-1 bg-gradient-to-r from-transparent via-blue-500 to-transparent opacity-50 blur-sm"></div>
            <h4 className="text-cyan-400 font-bold tracking-widest uppercase text-xs mb-3 mt-4">Key Capabilities</h4>
            <h2 className="text-3xl md:text-5xl font-bold text-white mb-4 drop-shadow-md">From Detection to Decision</h2>
            <p className="text-slate-400 max-w-2xl mx-auto">A unified platform for real-time airspace awareness and critical infrastructure protection.</p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 perspective-[1000px]">
            {/* Cards with 3D Hover & Glow */}
            {[
              { title: 'Multi-Sensor Fusion', desc: 'Combine radar, EO/IR, RF, and IoT data into a single, coherent picture.', icon: Crosshair, color: 'cyan' },
              { title: 'AI-Powered Tracking', desc: 'Detect, classify, and track drones and other aerial objects in real time.', icon: Cpu, color: 'violet' },
              { title: 'Real-Time Alerts', desc: 'Get instant notifications for unauthorized activity and escalating threats.', icon: ShieldAlert, color: 'red' },
              { title: '3D Digital Twin', desc: 'Visualize your sites, assets, zones, and live tracks in 3D.', icon: Map, color: 'blue' }
            ].map((cap, i) => (
              <div key={i} className={`group bg-slate-900/50 border border-slate-800 p-6 rounded-2xl hover:bg-slate-800 transition-all duration-500 cursor-pointer relative overflow-hidden transform hover:-translate-y-2 hover:rotate-y-[5deg] hover:shadow-[0_20px_40px_rgba(0,0,0,0.4)]`}>
                <div className={`absolute top-0 left-0 w-full h-1 bg-${cap.color}-500/50 opacity-0 group-hover:opacity-100 transition-opacity duration-500 shadow-[0_0_15px_rgba(0,0,0,1)]`}></div>
                <div className="absolute -right-8 -top-8 w-32 h-32 bg-white/5 rounded-full blur-[40px] group-hover:bg-white/10 transition-colors"></div>
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-6 border bg-${cap.color}-500/10 border-${cap.color}-500/30 group-hover:scale-110 group-hover:rotate-6 transition-all duration-300`}>
                  <cap.icon className={`w-6 h-6 text-${cap.color}-400`} />
                </div>
                <h3 className="text-lg font-bold text-white mb-2 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-white group-hover:to-slate-400">{cap.title}</h3>
                <p className="text-slate-400 text-sm leading-relaxed relative z-10">{cap.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* SECTION D - Digital Twin Showcase */}
      <section id="digital-twin" className="py-24 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-slate-950 to-slate-900 z-0"></div>
        <div className="max-w-7xl mx-auto px-6 relative z-10 flex flex-col lg:flex-row items-center gap-16">
          <div className="lg:w-1/3">
            <h4 className="text-blue-500 font-bold tracking-widest uppercase text-xs mb-3">Live Digital Twin</h4>
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">See More.<br/>Respond Faster.</h2>
            <p className="text-slate-400 mb-8 leading-relaxed">
              AEROSHIELD creates a dynamic 3D digital twin of your operational environments, overlaying live sensor data, drone tracks, restricted zones, and critical assets on a real-world map.
            </p>
            
            <ul className="space-y-4 mb-10">
              {['Interactive 3D map with live tracks', 'Sites, assets and restricted zones', 'Real-time sensor and alert overlays', 'Historical playback and analysis'].map((item, i) => (
                <li key={i} className="flex items-start gap-3 group">
                  <div className="bg-blue-900/30 rounded-full p-1 group-hover:bg-blue-500/30 transition-colors shrink-0 mt-0.5">
                    <CheckCircle className="w-4 h-4 text-blue-400" />
                  </div>
                  <span className="text-slate-300 group-hover:text-white transition-colors">{item}</span>
                </li>
              ))}
            </ul>

            <button onClick={() => navigate('/login')} className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white px-6 py-3 rounded-lg font-semibold transition-all shadow-[0_0_20px_rgba(37,99,235,0.4)] hover:shadow-[0_0_30px_rgba(37,99,235,0.6)] hover:-translate-y-1">
              Explore the Digital Twin <ChevronRight className="w-4 h-4" />
            </button>
          </div>
          
          <div className="lg:w-2/3 w-full perspective-[1500px]">
            <div className="rounded-2xl overflow-hidden border border-slate-700 bg-slate-900 shadow-[0_30px_60px_rgba(0,0,0,0.6)] transform transition-transform duration-700 hover:rotate-y-[2deg] hover:rotate-x-[1deg] hover:scale-[1.02] cursor-pointer" onClick={() => navigate('/login')}>
              <div className="h-12 bg-slate-950 border-b border-slate-800 flex items-center justify-between px-4">
                <div className="flex items-center gap-2 text-slate-400">
                  <Shield className="w-5 h-5 text-blue-500" /> AEROSHIELD / Twin
                </div>
                <div className="flex gap-2">
                  <div className="w-3 h-3 rounded-full bg-slate-800 hover:bg-red-500 transition-colors"></div>
                  <div className="w-3 h-3 rounded-full bg-slate-800 hover:bg-yellow-500 transition-colors"></div>
                  <div className="w-3 h-3 rounded-full bg-slate-800 hover:bg-green-500 transition-colors"></div>
                </div>
              </div>
              
              <div className="flex h-[500px]">
                <div className="w-48 border-r border-slate-800 bg-slate-900/80 p-4 hidden md:block">
                  <div className="space-y-4">
                    {['Overview', 'Digital Twin', 'Sites', 'Assets', 'Sensors'].map((l, i) => (
                      <div key={i} className={`text-sm cursor-pointer p-2 rounded transition-colors ${i===1 ? 'bg-blue-600/20 text-blue-400 font-medium border border-blue-500/20' : 'text-slate-500 hover:bg-slate-800'}`}>{l}</div>
                    ))}
                  </div>
                </div>
                
                {/* Map image mockup (Satellite at night) */}
                <div className="flex-1 relative bg-slate-900 pointer-events-none overflow-hidden">
                   <img src="https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&q=80" alt="Satellite Map view" className="w-full h-full object-cover opacity-80 mix-blend-screen hue-rotate-180 brightness-125 contrast-125" />
                   {/* Fake Tracks on Map - shifted to India coordinates roughly */}
                   <div className="absolute top-[45%] left-[40%]">
                     <div className="w-4 h-4 rounded-full bg-red-500 shadow-[0_0_15px_rgba(239,68,68,1)] animate-ping absolute"></div>
                     <div className="w-4 h-4 rounded-full bg-red-500 shadow-[0_0_15px_rgba(239,68,68,1)] relative"></div>
                   </div>
                   <div className="absolute top-[65%] left-[45%]">
                     <div className="w-3 h-3 rounded-full bg-green-500 shadow-[0_0_15px_rgba(34,197,94,1)]"></div>
                   </div>
                   {/* Fake Zone Overlay - over western India */}
                   <div className="absolute top-[35%] left-[30%] w-[15%] h-[25%] bg-red-500/10 border border-red-500/30 rounded-lg backdrop-blur-[1px]"></div>
                </div>
                
                <div className="w-64 border-l border-slate-800 bg-slate-900/90 backdrop-blur p-4 hidden lg:block">
                   <h3 className="text-white text-sm font-semibold mb-4">Active Tracks (2)</h3>
                   <div className="bg-slate-800 border border-slate-700 rounded p-3 mb-3 hover:border-red-500/50 transition-colors shadow-lg">
                     <div className="flex justify-between items-center mb-1">
                       <span className="text-red-400 font-mono text-xs">TRK-992</span>
                       <span className="bg-red-500/20 text-red-500 text-[10px] px-1.5 rounded animate-pulse">HIGH</span>
                     </div>
                     <div className="text-slate-300 text-sm">Unknown Drone</div>
                   </div>
                   <div className="bg-slate-800 border border-slate-700 rounded p-3 hover:border-green-500/50 transition-colors shadow-lg">
                     <div className="flex justify-between items-center mb-1">
                       <span className="text-green-400 font-mono text-xs">TRK-814</span>
                       <span className="bg-green-500/20 text-green-500 text-[10px] px-1.5 rounded">SAFE</span>
                     </div>
                     <div className="text-slate-300 text-sm">Auth Quadcopter</div>
                   </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION E - Use Cases (Pure CSS/Gradients to ensure 100% reliability and 3D feel) */}
      <section id="use-cases" className="py-24 bg-slate-950 border-t border-slate-900">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h4 className="text-cyan-400 font-bold tracking-widest uppercase text-xs mb-3">Real-World Impact</h4>
            <h2 className="text-3xl md:text-5xl font-bold text-white mb-4">Protecting Critical Infrastructure</h2>
            <p className="text-slate-400 max-w-2xl mx-auto">AEROSHIELD helps organizations detect, track, and respond to drone threats across a wide range of sectors.</p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              { title: 'Power & Energy', desc: 'Protect power plants, substations and renewable energy assets.', img: '/images/real_power_1791618000820.jpg' },
              { title: 'Transport & Logistics', desc: 'Secure airports, ports, railways and logistics hubs.', img: '/images/real_transport_1791618013897.jpg' },
              { title: 'Industrial Facilities', desc: 'Monitor refineries, manufacturing sites and industrial complexes.', img: '/images/real_industrial_1791618037572.jpg' },
              { title: 'Government & Defense', desc: 'Safeguard military bases, government facilities, and sensitive sites.', img: '/images/real_defense_1791618051506.jpg' },
              { title: 'Communications', desc: 'Protect telecom towers, broadcast facilities and data centers.', img: '/images/real_communications_1791618070663.jpg' },
              { title: 'Healthcare', desc: 'Secure hospitals, research facilities and healthcare infrastructure.', img: '/images/healthcare_1791617805886.jpg' }
            ].map((uc, i) => (
              <div key={i} className="group rounded-2xl overflow-hidden border border-slate-800 bg-slate-900 hover:border-blue-500/50 transition-all duration-300 cursor-pointer shadow-lg hover:shadow-[0_20px_40px_rgba(37,99,235,0.2)] hover:-translate-y-2">
                <div className="h-48 relative overflow-hidden bg-slate-800">
                  <img src={uc.img} alt={uc.title} className="w-full h-full object-cover transform group-hover:scale-105 transition-all duration-700 ease-out" />
                  <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-transparent to-transparent opacity-90 group-hover:opacity-70 transition-opacity duration-300 z-10"></div>
                </div>
                <div className="p-6 relative bg-slate-900 z-20 border-t border-slate-800/50 group-hover:border-blue-500/30 transition-colors">
                  <h3 className="text-white font-bold mb-2 text-lg group-hover:text-blue-400 transition-colors">{uc.title}</h3>
                  <p className="text-slate-400 text-sm leading-relaxed">{uc.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* SECTION F & G - Security and Tech Stack */}
      <section id="technology" className="py-24 bg-slate-900 border-y border-slate-800 relative overflow-hidden">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#1e293b_1px,transparent_1px),linear-gradient(to_bottom,#1e293b_1px,transparent_1px)] bg-[size:3rem_3rem] opacity-20"></div>
        <div className="absolute inset-0 bg-gradient-to-b from-slate-950 via-transparent to-slate-950 pointer-events-none"></div>
        
        <div className="max-w-7xl mx-auto px-6 relative z-10">
          
          <div className="text-center mb-16">
            <h4 className="text-blue-500 font-bold tracking-widest uppercase text-xs mb-3">Secure By Design</h4>
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">Built for Secure Operational Environments</h2>
            <p className="text-slate-400 max-w-2xl mx-auto">AEROSHIELD is designed with security, reliability and scalability in mind, ready for deployment in mission-critical environments.</p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-6 lg:gap-8 mb-24">
            {[
              { title: 'Role-Based Access\nControl (RBAC)', icon: Shield },
              { title: 'Encrypted Data\nIn Transit & At Rest', icon: Lock },
              { title: 'Audit & Compliance\nReady', icon: Check },
              { title: 'On-Prem or Cloud\nDeployment', icon: Cloud },
              { title: 'Scalable Architecture', icon: Layers },
              { title: 'API-First Integration', icon: Navigation }
            ].map((item, i) => (
              <div key={i} className="flex flex-col items-center text-center p-6 bg-slate-950/60 rounded-2xl border border-slate-800 backdrop-blur hover:bg-slate-800 hover:shadow-[0_15px_30px_rgba(16,185,129,0.05)] transition-all duration-300">
                <div className="w-16 h-16 rounded-full flex items-center justify-center mb-4 text-emerald-400">
                  <item.icon className="w-8 h-8 drop-shadow-[0_0_10px_rgba(52,211,153,0.5)]" />
                </div>
                <h3 className="text-slate-200 font-semibold text-sm whitespace-pre-line">{item.title}</h3>
              </div>
            ))}
          </div>

          <div className="text-center mb-12">
            <h4 className="text-blue-500 font-bold tracking-widest uppercase text-xs mb-3">Technology Stack</h4>
            <h2 className="text-3xl font-bold text-white mb-4">Modern. Open. Extensible.</h2>
            <p className="text-slate-400">Built with proven open-source technologies and industry standards.</p>
          </div>

          <div className="flex flex-wrap justify-center gap-4">
            {[
              { name: 'FastAPI', sub: 'Backend API', icon: Zap, color: 'text-emerald-400' },
              { name: 'PostgreSQL\n+ PostGIS', sub: 'Spatial Database', icon: Database, color: 'text-blue-400' },
              { name: 'Redis', sub: 'Caching & Events', icon: Server, color: 'text-red-400' },
              { name: 'React', sub: 'Frontend', icon: Cpu, color: 'text-cyan-400' },
              { name: 'MapLibre', sub: '3D Mapping', icon: Map, color: 'text-emerald-500' },
              { name: 'Python', sub: 'Analytics & ML', icon: Search, color: 'text-yellow-400' }
            ].map((tech, i) => (
              <div key={i} className="flex flex-col items-center justify-center px-6 py-4 bg-slate-950/80 border border-slate-800 rounded-xl text-center min-w-[140px] hover:border-blue-500/50 hover:bg-slate-800/80 transition-all cursor-pointer">
                <tech.icon className={`w-8 h-8 mb-3 ${tech.color}`} />
                <div className="text-white font-bold tracking-wide text-sm whitespace-pre-line leading-tight">{tech.name}</div>
                <div className="text-slate-500 text-[10px] mt-2 uppercase tracking-wider">{tech.sub}</div>
              </div>
            ))}
          </div>

        </div>
      </section>

      {/* SECTION H - Conversion CTA */}
      <section className="py-32 relative overflow-hidden flex items-center justify-center min-h-[60vh]">
        <div className="absolute inset-0 bg-slate-950 z-0"></div>
        
        {/* The CTA Background image showing SOC monitors */}
        <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80')] bg-cover bg-center opacity-30 mix-blend-luminosity z-0"></div>
        <div className="absolute inset-0 bg-gradient-to-r from-slate-950 via-slate-950/80 to-transparent z-10"></div>
        
        <div className="max-w-7xl mx-auto px-6 relative z-20 w-full flex flex-col md:flex-row items-center justify-between gap-12">
          <div className="max-w-xl">
            <h4 className="text-blue-500 font-bold tracking-widest uppercase text-xs mb-3">Get Started</h4>
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6 drop-shadow-lg">Ready to Secure Your Skies?</h2>
            <p className="text-lg text-slate-300 mb-10">Deploy AEROSHIELD in your environment and gain real-time visibility and control over aerial threats.</p>
            
            <div className="flex flex-col sm:flex-row items-center gap-4">
              <button onClick={() => navigate('/login')} className="w-full sm:w-auto bg-blue-600 hover:bg-blue-500 text-white px-8 py-3 rounded-lg font-bold transition-all shadow-[0_0_20px_rgba(37,99,235,0.4)] hover:shadow-[0_0_30px_rgba(37,99,235,0.7)] hover:-translate-y-1">
                Get Started &rarr;
              </button>
              <button onClick={() => navigate('/login')} className="w-full sm:w-auto bg-slate-800/80 hover:bg-slate-700 backdrop-blur text-white border border-slate-700 px-8 py-3 rounded-lg font-bold transition-all hover:-translate-y-1">
                Contact Us
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION I - Footer */}
      <footer className="bg-slate-950 py-12 border-t border-slate-900 relative">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
            <div className="col-span-1">
              <div className="flex items-center gap-2 mb-4">
                <Shield className="w-6 h-6 text-blue-500" />
                <span className="text-lg font-bold text-white">AEROSHIELD</span>
              </div>
              <p className="text-slate-500 text-sm leading-relaxed">
                AI-powered airspace awareness for a safer tomorrow.
              </p>
            </div>
            
            <div>
              <h4 className="text-white font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-sm text-slate-400">
                <li><a href="#features" className="hover:text-blue-400 transition-colors">Features</a></li>
                <li><a href="#digital-twin" className="hover:text-blue-400 transition-colors">Digital Twin</a></li>
                <li><a href="#use-cases" className="hover:text-blue-400 transition-colors">Use Cases</a></li>
                <li><a href="#technology" className="hover:text-blue-400 transition-colors">Technology</a></li>
              </ul>
            </div>

            <div>
              <h4 className="text-white font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-slate-400">
                <li><a href="#" className="hover:text-blue-400 transition-colors">About</a></li>
                <li><a href="#" className="hover:text-blue-400 transition-colors">Careers</a></li>
                <li><a href="#" className="hover:text-blue-400 transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-blue-400 transition-colors">Contact</a></li>
              </ul>
            </div>

            <div>
              <h4 className="text-white font-semibold mb-4">Resources</h4>
              <ul className="space-y-2 text-sm text-slate-400">
                <li><a href="#" className="hover:text-blue-400 transition-colors">Documentation</a></li>
                <li><a href="#" className="hover:text-blue-400 transition-colors">API Reference</a></li>
                <li><a href="#" className="hover:text-blue-400 transition-colors">Support</a></li>
                <li><a href="#" className="hover:text-blue-400 transition-colors">Status</a></li>
              </ul>
            </div>
          </div>
          
          <div className="pt-8 border-t border-slate-800 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-slate-500">
            <div>&copy; 2026 AEROSHIELD. All rights reserved.</div>
            <div className="flex gap-4">
              <a href="#" className="hover:text-white transition-colors">Privacy Policy</a>
              <a href="#" className="hover:text-white transition-colors">Terms of Service</a>
              <a href="#" className="hover:text-white transition-colors">Security</a>
            </div>
          </div>
        </div>
      </footer>

    </div>
  );
};
