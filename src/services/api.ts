import { Vehicle, SearchParams } from '@/types/vehicle';

const API_BASE_URL = import.meta.env.VITE_RAILWAY_API_URL || 'http://localhost:8000';

export const searchVehicles = async (
  params: SearchParams,
  onProgress?: (current: number, total: number, site: string) => void
): Promise<Vehicle[]> => {
  const response = await fetch(`${API_BASE_URL}/api/search`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(params),
  });

  if (!response.ok) {
    throw new Error(`Search failed: ${response.statusText}`);
  }

  const reader = response.body?.getReader();
  if (!reader) {
    throw new Error('Stream not available');
  }

  const decoder = new TextDecoder();
  const vehicles: Vehicle[] = [];
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    
    if (done) break;
    
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';

    for (const line of lines) {
      if (line.trim().startsWith('data: ')) {
        try {
          const data = JSON.parse(line.slice(6));
          
          if (data.type === 'progress' && onProgress) {
            onProgress(data.current, data.total, data.site);
          } else if (data.type === 'result') {
            vehicles.push(data.vehicle);
          }
        } catch (e) {
          console.error('Failed to parse SSE data:', e);
        }
      }
    }
  }

  return vehicles;
};

export const exportToExcel = (vehicles: Vehicle[]): void => {
  const headers = ['Source', 'Title', 'Price', 'Location', 'URL'];
  const rows = vehicles.map(v => [
    v.source,
    v.title,
    `$${v.price.toLocaleString()}`,
    v.location,
    v.url
  ]);

  const csv = [
    headers.join(','),
    ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
  ].join('\n');

  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `carfinder-results-${new Date().toISOString().split('T')[0]}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};
