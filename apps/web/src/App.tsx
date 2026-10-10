import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Landing } from './pages/Landing';
import { DigitalTwin } from './pages/DigitalTwin';
import { Login } from './pages/Login';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/twin" element={<DigitalTwin />} />
      </Routes>
    </Router>
  );
}

export default App;
