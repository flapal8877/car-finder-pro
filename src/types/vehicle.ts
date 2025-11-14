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
