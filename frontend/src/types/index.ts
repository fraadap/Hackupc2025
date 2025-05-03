export interface User {
  email: string;
  username: string;
}

export interface UserCreate {
  email: string;
  username: string;
  password: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
}

export interface CityCategory {
  category: string;
  value: number;
  descr: string;
}

export interface City {
  name: string;
  categories: CityCategory[];
}

export interface Vote {
  city: string;
  value: number; // 0 or 1
}

export interface Group {
  code: number;
  members: string[];
}

export interface GroupCreate {
  code?: number;
}

export interface Flight {
  code: number;
  cost: number;
  depCity: string;
  arrCity: string;
  depTime: string;
  timeDuration: number;
  distance: number;
  planeModel: string;
  company: string;
}

export interface FlightSearch {
  departure_city: string;
  min_date: string;
  max_date: string;
  max_budget?: number;
  companies?: string[];
} 