import axios from 'axios';
import { 
  User, 
  UserCreate, 
  AuthToken, 
  City, 
  Vote, 
  Group, 
  GroupCreate, 
  Flight, 
  FlightSearch 
} from '../types';

const API_URL = 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Authentication
export const login = async (email: string, password: string): Promise<AuthToken> => {
  const formData = new FormData();
  formData.append('username', email); // Backend expects 'username' field for email
  formData.append('password', password);
  
  const response = await axios.post<AuthToken>(`${API_URL}/token`, formData);
  return response.data;
};

export const register = async (userData: UserCreate): Promise<User> => {
  const response = await api.post<User>('/users', userData);
  return response.data;
};

export const getCurrentUser = async (): Promise<User> => {
  const response = await api.get<User>('/users/me');
  return response.data;
};

// Cities
export const getCities = async (): Promise<string[]> => {
  const response = await api.get<string[]>('/cities');
  return response.data;
};

export const getCity = async (cityName: string): Promise<City> => {
  const response = await api.get<City>(`/cities/${cityName}`);
  return response.data;
};

export const getCitiesForEvaluation = async (limit: number = 5): Promise<City[]> => {
  const response = await api.get<City[]>(`/cities/evaluation?limit=${limit}`);
  return response.data;
};

export const voteCity = async (vote: Vote): Promise<{ status: string }> => {
  const response = await api.post<{ status: string }>('/cities/vote', vote);
  return response.data;
};

export const getRecommendations = async (limit: number = 10): Promise<City[]> => {
  const response = await api.get<City[]>(`/recommendations?limit=${limit}`);
  return response.data;
};

// Groups
export const createGroup = async (group: GroupCreate): Promise<Group> => {
  const response = await api.post<Group>('/groups', group);
  return response.data;
};

export const joinGroup = async (code: number): Promise<Group> => {
  const response = await api.post<Group>('/groups/join', { group_code: code });
  return response.data;
};

export const getUserGroups = async (): Promise<Group[]> => {
  const response = await api.get<Group[]>('/groups');
  return response.data;
};

export const getGroupRecommendations = async (groupCode: number, limit: number = 10): Promise<City[]> => {
  const response = await api.get<City[]>(`/groups/${groupCode}/recommendations?limit=${limit}`);
  return response.data;
};

// Flights
export const searchFlights = async (search: FlightSearch): Promise<Flight[]> => {
  const response = await api.post<Flight[]>('/flights/search', search);
  return response.data;
};

export const getFlightCompanies = async (): Promise<string[]> => {
  const response = await api.get<string[]>('/flight_companies');
  return response.data;
};

export default api; 