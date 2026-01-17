import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface User {
  username: string;
  email: string;
  pin: string;
}

export interface Contact {
  name: string;
  relation: string;
  phone: string;
}

export interface Location {
  latitude: number;
  longitude: number;
  accuracy: number;
  timestamp?: string;
}

export interface RiskAnalysis {
  risk_level: 'low' | 'medium' | 'high';
  safe: boolean;
  message?: string;
}

export const apiService = {
  // Health check
  ping: async () => {
    const response = await api.get('/ping');
    return response.data;
  },

  // User endpoints
  register: async (username: string, password: string, email: string, pin: string) => {
    const response = await api.post('/register', { username, password, email, pin });
    return response.data;
  },

  getUser: async (username: string) => {
    const response = await api.get(`/user/${username}`);
    return response.data;
  },

  // Contact endpoints
  addContact: async (username: string, name: string, relation: string, phone: string) => {
    const response = await api.post('/contact', { username, name, relation, phone });
    return response.data;
  },

  getContacts: async (username: string) => {
    const response = await api.get(`/contacts/${username}`);
    return response.data;
  },

  // Location endpoints
  analyzeLocation: async (username: string, latitude: number, longitude: number, accuracy: number) => {
    const response = await api.post('/analyze', { username, latitude, longitude, accuracy });
    return response.data as RiskAnalysis;
  },

  getLocations: async (username: string, limit: number = 50) => {
    const response = await api.get(`/locations/${username}?limit=${limit}`);
    return response.data;
  },

  // SOS endpoint
  triggerSOS: async (username: string, latitude: number, longitude: number, accuracy: number) => {
    const response = await api.post('/sos', { username, latitude, longitude, accuracy });
    return response.data;
  },
};

export default api;
