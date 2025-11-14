export interface Vehicle {
  id: string;
  source: string;
  title: string;
  price: number;
  location: string;
  url: string;
  imageUrl?: string;
  description?: string;
  timestamp: string;
}

export interface SearchParams {
  keyword: string;
  location: string;
  maxPrice: number;
  make?: string;
  model?: string;
  minYear?: number;
  maxYear?: number;
  maxMileage?: number;
  zipCode?: string;
  radius?: number;
  bodyStyles?: string[];
  condition?: string;
  fuelTypes?: string[];
  privateOnly?: boolean;
  searchMode?: 'fast' | 'full';
}

export interface SearchProgress {
  current: number;
  total: number;
  currentSite: string;
  status: 'idle' | 'searching' | 'complete' | 'error';
}

export interface ApiConfig {
  baseUrl: string;
}
