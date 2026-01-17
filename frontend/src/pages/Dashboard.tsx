import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { AlertCircle, MapPin, Shield, Users } from 'lucide-react';

interface DashboardProps {
  username: string;
  onLogout: () => void;
}

export const Dashboard: React.FC<DashboardProps> = ({ username, onLogout }) => {
  const [activeTab, setActiveTab] = useState<'safety' | 'contacts' | 'history'>('safety');
  const [riskLevel, setRiskLevel] = useState<string>('unknown');
  const [location, setLocation] = useState<{ lat: number; lng: number } | null>(null);
  const [contacts, setContacts] = useState<any[]>([]);
  const [locations, setLocations] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Get current location
  const getLocation = () => {
    if (navigator.geolocation) {
      setLoading(true);
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const { latitude, longitude, accuracy } = position.coords;
          setLocation({ lat: latitude, lng: longitude });

          try {
            const analysis = await apiService.analyzeLocation(username, latitude, longitude, accuracy);
            setRiskLevel(analysis.risk_level);
          } catch (err) {
            setError('Failed to analyze location');
          } finally {
            setLoading(false);
          }
        },
        () => setError('Failed to get location. Enable location services.')
      );
    }
  };

  // Fetch contacts
  const fetchContacts = async () => {
    try {
      setLoading(true);
      const data = await apiService.getContacts(username);
      setContacts(data);
    } catch (err) {
      setError('Failed to fetch contacts');
    } finally {
      setLoading(false);
    }
  };

  // Fetch location history
  const fetchLocations = async () => {
    try {
      setLoading(true);
      const data = await apiService.getLocations(username, 20);
      setLocations(data);
    } catch (err) {
      setError('Failed to fetch location history');
    } finally {
      setLoading(false);
    }
  };

  // Trigger SOS
  const triggerSOS = async () => {
    if (!location) {
      setError('Location required for SOS. Please enable location services.');
      return;
    }

    if (window.confirm('Trigger emergency SOS? Emergency contacts will be notified!')) {
      try {
        setLoading(true);
        await apiService.triggerSOS(username, location.lat, location.lng, 10);
        setError('');
        alert('SOS alert sent to emergency contacts!');
      } catch (err) {
        setError('Failed to send SOS alert');
      } finally {
        setLoading(false);
      }
    }
  };

  useEffect(() => {
    if (activeTab === 'safety') {
      getLocation();
    } else if (activeTab === 'contacts') {
      fetchContacts();
    } else if (activeTab === 'history') {
      fetchLocations();
    }
  }, [activeTab]);

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-red-600 text-white p-6 shadow-lg">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold">SAFEHER</h1>
            <p className="text-red-100">Welcome, {username}</p>
          </div>
          <button
            onClick={onLogout}
            className="px-4 py-2 bg-red-700 hover:bg-red-800 rounded-lg font-semibold transition"
          >
            Logout
          </button>
        </div>
      </div>

      {/* SOS Button */}
      <div className="max-w-6xl mx-auto mt-6 px-6">
        <button
          onClick={triggerSOS}
          disabled={loading}
          className="w-full bg-red-700 hover:bg-red-800 text-white font-bold py-4 px-6 rounded-lg text-2xl shadow-lg transition disabled:opacity-50"
        >
          🚨 EMERGENCY SOS 🚨
        </button>
      </div>

      {/* Error message */}
      {error && (
        <div className="max-w-6xl mx-auto mt-4 px-6">
          <div className="p-4 bg-red-50 border-l-4 border-red-600 flex gap-2">
            <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0" />
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="max-w-6xl mx-auto mt-6 px-6">
        <div className="flex gap-2 border-b border-gray-300">
          <button
            onClick={() => setActiveTab('safety')}
            className={`px-6 py-3 font-semibold flex items-center gap-2 border-b-2 transition ${
              activeTab === 'safety'
                ? 'border-red-600 text-red-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            <Shield className="w-5 h-5" />
            Safety Check
          </button>
          <button
            onClick={() => setActiveTab('contacts')}
            className={`px-6 py-3 font-semibold flex items-center gap-2 border-b-2 transition ${
              activeTab === 'contacts'
                ? 'border-red-600 text-red-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            <Users className="w-5 h-5" />
            Contacts
          </button>
          <button
            onClick={() => setActiveTab('history')}
            className={`px-6 py-3 font-semibold flex items-center gap-2 border-b-2 transition ${
              activeTab === 'history'
                ? 'border-red-600 text-red-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            <MapPin className="w-5 h-5" />
            Location History
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-6xl mx-auto mt-6 px-6 mb-10">
        {/* Safety Check Tab */}
        {activeTab === 'safety' && (
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold mb-6">Safety Check</h2>
            {location ? (
              <div className="space-y-4">
                <p className="text-gray-700">
                  <strong>Your Location:</strong> {location.lat.toFixed(4)}, {location.lng.toFixed(4)}
                </p>
                <div
                  className={`p-6 rounded-lg text-center ${
                    riskLevel === 'low'
                      ? 'bg-green-50 border-2 border-green-600'
                      : riskLevel === 'medium'
                      ? 'bg-yellow-50 border-2 border-yellow-600'
                      : 'bg-red-50 border-2 border-red-600'
                  }`}
                >
                  <p className="text-sm font-semibold text-gray-700 mb-2">RISK LEVEL</p>
                  <p
                    className={`text-4xl font-bold ${
                      riskLevel === 'low'
                        ? 'text-green-600'
                        : riskLevel === 'medium'
                        ? 'text-yellow-600'
                        : riskLevel === 'high'
                        ? 'text-red-600'
                        : 'text-gray-600'
                    }`}
                  >
                    {riskLevel.toUpperCase()}
                  </p>
                </div>
              </div>
            ) : (
              <p className="text-gray-600">Enable location services to check safety</p>
            )}
          </div>
        )}

        {/* Contacts Tab */}
        {activeTab === 'contacts' && (
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold mb-6">Emergency Contacts</h2>
            {contacts.length > 0 ? (
              <div className="grid gap-4">
                {contacts.map((contact, idx) => (
                  <div key={idx} className="p-4 border border-gray-300 rounded-lg">
                    <p className="font-semibold text-lg">{contact.name}</p>
                    <p className="text-gray-600">{contact.relation}</p>
                    <p className="text-gray-600">{contact.phone}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-600">No contacts added yet</p>
            )}
          </div>
        )}

        {/* Location History Tab */}
        {activeTab === 'history' && (
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold mb-6">Location History</h2>
            {locations.length > 0 ? (
              <div className="grid gap-4">
                {locations.map((loc, idx) => (
                  <div key={idx} className="p-4 border border-gray-300 rounded-lg">
                    <p className="text-sm text-gray-500">{loc.timestamp}</p>
                    <p className="text-gray-700">
                      {loc.latitude.toFixed(4)}, {loc.longitude.toFixed(4)}
                    </p>
                    <p className="text-sm text-gray-600">Accuracy: ±{loc.accuracy}m</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-600">No location history</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
