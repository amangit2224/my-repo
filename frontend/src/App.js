import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import History from './pages/History';
import ReportDetails from './pages/ReportDetails';
import JargonBuster from './pages/JargonBuster';
import HealthTrends from './pages/HealthTrends';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';
import HealthRiskAssessment from './pages/HealthRiskAssessment';
import NearbyDoctors from './pages/NearbyDoctors';

import './App.css';

function App() {
  const [darkMode, setDarkMode] = useState(
    localStorage.getItem('darkMode') === 'true'
  );

  useEffect(() => {
    document.body.classList.toggle('dark-mode', darkMode);
    localStorage.setItem('darkMode', darkMode);
  }, [darkMode]);

  const ProtectedRoute = ({ children }) => {
    const token = localStorage.getItem('token');
    return token ? children : <Navigate to="/login" replace />;
  };

  return (
    <Router>
      <Routes>
        {/* Public */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />

        {/* Protected */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard darkMode={darkMode} setDarkMode={setDarkMode} />
            </ProtectedRoute>
          }
        />

        <Route
          path="/history"
          element={
            <ProtectedRoute>
              <History darkMode={darkMode} setDarkMode={setDarkMode} />
            </ProtectedRoute>
          }
        />

        <Route
          path="/report/:reportId"
          element={
            <ProtectedRoute>
              <ReportDetails darkMode={darkMode} setDarkMode={setDarkMode} />
            </ProtectedRoute>
          }
        />

        <Route
          path="/risk-assessment/:reportId"
          element={
            <ProtectedRoute>
              <HealthRiskAssessment darkMode={darkMode} setDarkMode={setDarkMode} />
            </ProtectedRoute>
          }
        />

        <Route
          path="/jargon"
          element={
            <ProtectedRoute>
              <JargonBuster darkMode={darkMode} setDarkMode={setDarkMode} />
            </ProtectedRoute>
          }
        />

        <Route
          path="/health"
          element={
            <ProtectedRoute>
              <HealthTrends darkMode={darkMode} setDarkMode={setDarkMode} />
            </ProtectedRoute>
          }
        />

        <Route
          path="/nearby-doctors"
          element={
            <ProtectedRoute>
              <NearbyDoctors darkMode={darkMode} setDarkMode={setDarkMode} />
            </ProtectedRoute>
          }
        />

        {/* Defaults */}
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
