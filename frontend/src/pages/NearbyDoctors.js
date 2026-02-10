import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import '../App.css';

// Fix Leaflet default marker icon issue
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

// Custom hospital icon (kept red as in original)
const hospitalIcon = new L.Icon({
  iconUrl: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAiIGhlaWdodD0iMzAiIHZpZXdCb3g9IjAgMCAyMCAyMCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSIxMCIgY3k9IjEwIiByPSI5IiBmaWxsPSIjRUY0NDQ0Ii8+PHBhdGggZD0iTTEwIDZWMTRNNiAxMEgxNCIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz48L3N2Zz4=',
  iconSize: [30, 30],
  iconAnchor: [15, 30],
  popupAnchor: [0, -30],
});

function NearbyDoctors({ darkMode, setDarkMode }) {
  const navigate = useNavigate();
  const username = localStorage.getItem('username');
  
  const [userLocation, setUserLocation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedRadius, setSelectedRadius] = useState(5); // km
  const [filteredHospitals, setFilteredHospitals] = useState([]);

  // Hospitals near Banashankari 3rd Stage & PES University Ring Road Campus
  const hospitals = [
    {
      id: 1,
      name: "Kusuma Hospital",
      lat: 12.941983,
      lng: 77.550809,
      address: "10th Main Rd, 50 Feet Main Rd, Srinagar, Banashankari",
      rating: 4.5,
      phone: "+91 80 2326 5566",
      type: "Multi-Speciality",
      emergency: true
    },
    {
      id: 2,
      name: "AV Multi-speciality Hospital",
      lat: 12.932737,
      lng: 77.541092,
      address: "Hosakerehalli Main Rd, 6th Block, Banashankari 3rd Stage",
      rating: 4.2,
      phone: "+91 80 4242 5050",
      type: "Multi-Speciality",
      emergency: true
    },
    {
      id: 3,
      name: "ReLife Hospital",
      lat: 12.927900,
      lng: 77.546804,
      address: "100 feet ring road, 2nd Block, Banashankari 3rd Stage",
      rating: 4.6,
      phone: "+91 80 4155 5555",
      type: "Multi-Speciality",
      emergency: true
    },
    {
      id: 4,
      name: "Motherhood Hospital",
      lat: 12.926937,
      lng: 77.561086,
      address: "30th Main Rd, Banashankari 3rd Stage, Bengaluru",
      rating: 4.8,
      phone: "+91 80 6780 1680",
      type: "Maternity & Child Care",
      emergency: true
    },
    {
      id: 5,
      name: "Aarna Hospital",
      lat: 12.922109,
      lng: 77.543458,
      address: "Arav Arcade, 24th Cross, Banashankari 3rd Stage",
      rating: 4.8,
      phone: "+91 80 4212 1212",
      type: "Multi-Speciality",
      emergency: true
    },
    {
      id: 6,
      name: "Vinayaka Hospital",
      lat: 12.937519,
      lng: 77.549500,
      address: "80 Feet Rd, Mysore Bank Colony, Banashankari 1st Stage",
      rating: 4.3,
      phone: "+91 80 2689 3030",
      type: "Multi-Speciality",
      emergency: true
    },
    {
      id: 7,
      name: "Devagiri Hospital",
      lat: 12.924108,
      lng: 77.565804,
      address: "24th Cross Rd, Banashankari Stage II, Bengaluru",
      rating: 4.3,
      phone: "+91 98456 61188",
      type: "Multi-Speciality",
      emergency: true
    },
    {
      id: 8,
      name: "Bhagwan Mahaveer Jain Hospital",
      lat: 12.944252,
      lng: 77.537314,
      address: "3rd Main Rd, 1st phase Girinagar, Banashankari",
      rating: 4.7,
      phone: "+91 80 4042 4042",
      type: "Multi-Speciality",
      emergency: true
    },
    {
      id: 9,
      name: "People Tree Hospitals",
      lat: 12.942054,
      lng: 77.553603,
      address: "50 Feet Main Rd, Hanumanthnagar, Banashankari 1st Stage",
      rating: 4.4,
      phone: "+91 80 2661 5566",
      type: "Multi-Speciality",
      emergency: true
    },
    {
      id: 10,
      name: "ARHAM HOSPITALS",
      lat: 12.938316,
      lng: 77.556467,
      address: "7th cross, srinivasnagar, Banashankari 1st Stage",
      rating: 4.9,
      phone: "+91 80 4163 4163",
      type: "Multi-Speciality",
      emergency: true
    },
    {
      id: 11,
      name: "Sagar Hospitals - DSI",
      lat: 12.908123,
      lng: 77.564985,
      address: "Shavige Malleshwara Hills, Kumaraswamy Layout",
      rating: 4.4,
      phone: "+91 80 4299 9999",
      type: "Multi-Speciality",
      emergency: true
    },
    {
      id: 12,
      name: "Confido Multi Speciality Hospital",
      lat: 12.956304,
      lng: 77.546384,
      address: "Mysore Rd, near Veeranjaneya temple, Banashankari",
      rating: 4.5,
      phone: "+91 80 4610 0000",
      type: "Multi-Speciality",
      emergency: true
    },
    {
      id: 13,
      name: "Spandana Multi-Speciality Hospital",
      lat: 12.941746,
      lng: 77.526303,
      address: "Near Nayandahalli Metro Station, Mysore Road",
      rating: 4.4,
      phone: "+91 80 4242 4242",
      type: "Multi-Speciality",
      emergency: true
    },
    {
      id: 14,
      name: "Sanyra Hospital",
      lat: 12.922527,
      lng: 77.473821,
      address: "Kommaghatta Main Rd, Kengeri Satellite Town",
      rating: 4.8,
      phone: "+91 80 4112 2233",
      type: "Multi-Speciality",
      emergency: true
    },
    {
      id: 15,
      name: "Natus Women & Children Hospital",
      lat: 12.942688,
      lng: 77.525605,
      address: "Mysore Rd, Near Nayandahalli Metro Station",
      rating: 4.6,
      phone: "+91 80 4950 5050",
      type: "Maternity & Child Care",
      emergency: true
    }
  ];

  useEffect(() => {
    getUserLocation();
  }, []);

  useEffect(() => {
    if (userLocation) {
      filterHospitalsByRadius();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [userLocation, selectedRadius]);

  const getUserLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          });
          setLoading(false);
        },
        (error) => {
          console.error('Geolocation error:', error);
          // Fallback to Banashankari 3rd Stage center (near PES University)
          setUserLocation({
            lat: 12.9279,
            lng: 77.5468
          });
          setError('Using approximate location. Enable location for accurate results.');
          setLoading(false);
        }
      );
    } else {
      // Fallback to Banashankari 3rd Stage center (near PES University)
      setUserLocation({
        lat: 12.9279,
        lng: 77.5468
      });
      setError('Geolocation not supported. Showing Banashankari area hospitals.');
      setLoading(false);
    }
  };

  const calculateDistance = (lat1, lon1, lat2, lon2) => {
    const R = 6371; // Radius of Earth in km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = 
      Math.sin(dLat/2) * Math.sin(dLat/2) +
      Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
      Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
  };

  const filterHospitalsByRadius = () => {
    if (!userLocation) return;

    const hospitalsWithDistance = hospitals.map(hospital => ({
      ...hospital,
      distance: calculateDistance(
        userLocation.lat,
        userLocation.lng,
        hospital.lat,
        hospital.lng
      )
    }));

    const filtered = hospitalsWithDistance
      .filter(h => h.distance <= selectedRadius)
      .sort((a, b) => a.distance - b.distance);

    setFilteredHospitals(filtered);
  };

  const getDirections = (hospital) => {
    const url = `https://www.google.com/maps/dir/?api=1&destination=${hospital.lat},${hospital.lng}`;
    window.open(url, '_blank');
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    navigate('/login');
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  if (loading) {
    return (
      <div className="dashboard-wrapper">
        <nav className="modern-navbar">
          <div className="navbar-content">
            <div className="navbar-logo" onClick={() => navigate('/dashboard')}>
              <svg width="36" height="36" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="48" height="48" rx="12" fill="#2563EB"/>
                <rect x="14" y="10" width="20" height="28" rx="2" fill="white"/>
                <line x1="18" y1="16" x2="30" y2="16" stroke="#2563EB" strokeWidth="1.5" strokeLinecap="round"/>
                <line x1="18" y1="20" x2="30" y2="20" stroke="#2563EB" strokeWidth="1.5" strokeLinecap="round"/>
                <line x1="18" y1="24" x2="26" y2="24" stroke="#2563EB" strokeWidth="1.5" strokeLinecap="round"/>
                <circle cx="24" cy="31" r="4" fill="#2563EB"/>
                <path d="M24 29v4M22 31h4" stroke="white" strokeWidth="1.5" strokeLinecap="round"/>
              </svg>
              <span className="navbar-brand">MedLens</span>
            </div>

            <div className="navbar-links">
              <a href="/dashboard" className="nav-link">Dashboard</a>
              <a href="/history" className="nav-link">History</a>
              <a href="/health" className="nav-link">Analytics</a>
            </div>

            <div className="navbar-right">
              <button onClick={toggleDarkMode} className="icon-button">
                {darkMode ? (
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clipRule="evenodd"/>
                  </svg>
                ) : (
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"/>
                  </svg>
                )}
              </button>
              
              <button onClick={handleLogout} className="navbar-logout-btn">
                Logout
              </button>
              
              <div className="navbar-profile">
                <div className="profile-avatar">
                  {username?.charAt(0).toUpperCase()}
                </div>
              </div>
            </div>
          </div>
        </nav>

        <div className="modern-loading-state">
          <div className="loading-spinner"></div>
          <h3>Getting Your Location</h3>
          <p>Please allow location access to find nearby hospitals...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-wrapper">
      {/* Modern Navbar */}
      <nav className="modern-navbar">
        <div className="navbar-content">
          <div className="navbar-logo" onClick={() => navigate('/dashboard')}>
            <svg width="36" height="36" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="48" height="48" rx="12" fill="#2563EB"/>
              <rect x="14" y="10" width="20" height="28" rx="2" fill="white"/>
              <line x1="18" y1="16" x2="30" y2="16" stroke="#2563EB" strokeWidth="1.5" strokeLinecap="round"/>
              <line x1="18" y1="20" x2="30" y2="20" stroke="#2563EB" strokeWidth="1.5" strokeLinecap="round"/>
              <line x1="18" y1="24" x2="26" y2="24" stroke="#2563EB" strokeWidth="1.5" strokeLinecap="round"/>
              <circle cx="24" cy="31" r="4" fill="#2563EB"/>
              <path d="M24 29v4M22 31h4" stroke="white" strokeWidth="1.5" strokeLinecap="round"/>
            </svg>
            <span className="navbar-brand">MedLens</span>
          </div>

          <div className="navbar-links">
            <a href="/dashboard" className="nav-link">Dashboard</a>
            <a href="/history" className="nav-link">History</a>
            <a href="/health" className="nav-link">Analytics</a>
          </div>

          <div className="navbar-right">
            <button onClick={toggleDarkMode} className="icon-button">
              {darkMode ? (
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clipRule="evenodd"/>
                </svg>
              ) : (
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"/>
                </svg>
              )}
            </button>
            
            <button onClick={handleLogout} className="navbar-logout-btn">
              Logout
            </button>
            
            <div className="navbar-profile">
              <div className="profile-avatar">
                {username?.charAt(0).toUpperCase()}
              </div>
            </div>
          </div>
        </div>
      </nav>

      <div className="nearby-doctors-container">
        {/* Header */}
        <div className="nearby-header">
          <button onClick={() => navigate('/dashboard')} className="btn-back">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd"/>
            </svg>
            Back to Dashboard
          </button>
          <div className="nearby-title-section">
            <div className="nearby-icon">
              <svg width="32" height="32" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd"/>
              </svg>
            </div>
            <div>
              <h1>Find Nearby Doctors</h1>
              <p>Discover hospitals and clinics near you</p>
            </div>
          </div>
        </div>

        {error && (
          <div className="alert alert-warning">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd"/>
            </svg>
            {error}
          </div>
        )}

        {/* Filter Section */}
        <div className="filter-section">
          <label className="filter-label">
            <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M3 3a1 1 0 011-1h12a1 1 0 011 1v3a1 1 0 01-.293.707L12 11.414V15a1 1 0 01-.293.707l-2 2A1 1 0 018 17v-5.586L3.293 6.707A1 1 0 013 6V3z" clipRule="evenodd"/>
            </svg>
            Search Radius:
          </label>
          <div className="radius-buttons">
            {[2, 5, 10, 20].map(radius => (
              <button
                key={radius}
                onClick={() => setSelectedRadius(radius)}
                className={`radius-btn ${selectedRadius === radius ? 'active' : ''}`}
              >
                {radius} km
              </button>
            ))}
          </div>
          <span className="results-count">
            {filteredHospitals.length} hospitals found
          </span>
        </div>

        {/* Map Container */}
        <div className="map-container">
          {userLocation && (
            <MapContainer 
              center={[userLocation.lat, userLocation.lng]} 
              zoom={12} 
              style={{ height: '100%', width: '100%', borderRadius: '16px' }}
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              
              {/* User location marker */}
              <Circle
                center={[userLocation.lat, userLocation.lng]}
                radius={selectedRadius * 1000}
                pathOptions={{ color: '#3B82F6', fillColor: '#3B82F6', fillOpacity: 0.1 }}
              />
              <Marker position={[userLocation.lat, userLocation.lng]}>
                <Popup>Your Location</Popup>
              </Marker>

              {/* Hospital markers */}
              {filteredHospitals.map(hospital => (
                <Marker 
                  key={hospital.id}
                  position={[hospital.lat, hospital.lng]}
                  icon={hospitalIcon}
                >
                  <Popup>
                    <div style={{ minWidth: '200px' }}>
                      <h4 style={{ margin: '0 0 8px 0', fontSize: '14px' }}>{hospital.name}</h4>
                      <p style={{ margin: '4px 0', fontSize: '12px', color: '#666' }}>
                        ⭐ {hospital.rating} • {hospital.distance.toFixed(1)} km
                      </p>
                      <p style={{ margin: '4px 0', fontSize: '11px', color: '#888' }}>{hospital.type}</p>
                      <button 
                        onClick={() => getDirections(hospital)}
                        style={{
                          marginTop: '8px',
                          padding: '6px 12px',
                          background: '#3B82F6',
                          color: 'white',
                          border: 'none',
                          borderRadius: '6px',
                          cursor: 'pointer',
                          fontSize: '12px'
                        }}
                      >
                        Get Directions
                      </button>
                    </div>
                  </Popup>
                </Marker>
              ))}
            </MapContainer>
          )}
        </div>

        {/* Hospitals List */}
        <div className="hospitals-list">
          <h2>Nearby Hospitals ({filteredHospitals.length})</h2>
          
          {filteredHospitals.length === 0 ? (
            <div className="empty-state">
              <svg width="64" height="64" viewBox="0 0 20 20" fill="currentColor" style={{ opacity: 0.3 }}>
                <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd"/>
              </svg>
              <h3>No hospitals found</h3>
              <p>Try increasing the search radius</p>
            </div>
          ) : (
            <div className="hospitals-grid">
              {filteredHospitals.map(hospital => (
                <div key={hospital.id} className="hospital-card">
                  <div className="hospital-card-top">
                    <div className="hospital-icon">
                      <svg width="24" height="24" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.599-.8a1 1 0 01.894 1.79l-1.233.616 1.738 5.42a1 1 0 01-.285 1.05A3.989 3.989 0 0115 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.715-5.349L11 6.477V16h2a1 1 0 110 2H7a1 1 0 110-2h2V6.477L6.237 7.582l1.715 5.349a1 1 0 01-.285 1.05A3.989 3.989 0 015 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.738-5.42-1.233-.617a1 1 0 01.894-1.788l1.599.799L9 4.323V3a1 1 0 011-1z"/>
                      </svg>
                    </div>
                    
                    <div className="hospital-info">
                      <h3>{hospital.name}</h3>
                      <div className="hospital-meta">
                        <span className="hospital-rating">
                          ⭐ {hospital.rating}
                        </span>
                        <span className="hospital-distance">
                          📍 {hospital.distance.toFixed(1)} km
                        </span>
                        {hospital.emergency && (
                          <span className="hospital-emergency">
                            24/7 Emergency
                          </span>
                        )}
                      </div>
                      <p className="hospital-type">{hospital.type}</p>
                      <p className="hospital-address">{hospital.address}</p>
                      <p className="hospital-phone">📞 {hospital.phone}</p>
                    </div>
                  </div>

                  <button 
                    onClick={() => getDirections(hospital)}
                    className="btn-directions"
                  >
                    <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd"/>
                    </svg>
                    Get Directions
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default NearbyDoctors;