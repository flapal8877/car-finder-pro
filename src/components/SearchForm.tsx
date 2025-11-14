import { useState } from 'react';
import { Search } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { SearchParams } from '@/types/vehicle';

interface SearchFormProps {
  onSearch: (params: SearchParams) => void;
  isLoading: boolean;
}

export const SearchForm = ({ onSearch, isLoading }: SearchFormProps) => {
  const [keyword, setKeyword] = useState('');
  const [location, setLocation] = useState('');
  const [maxPrice, setMaxPrice] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch({
      keyword: keyword.trim(),
      location: location.trim(),
      maxPrice: parseInt(maxPrice) || 999999,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-2">
        <Label htmlFor="keyword">Search Keywords</Label>
        <Input
          id="keyword"
          type="text"
          placeholder="e.g., Honda Civic, Toyota Camry"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          required
          disabled={isLoading}
          className="bg-background/50 backdrop-blur-sm"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="location">Location</Label>
        <Input
          id="location"
          type="text"
          placeholder="e.g., Los Angeles, CA"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          required
          disabled={isLoading}
          className="bg-background/50 backdrop-blur-sm"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="maxPrice">Max Price ($)</Label>
        <Input
          id="maxPrice"
          type="number"
          placeholder="e.g., 25000"
          value={maxPrice}
          onChange={(e) => setMaxPrice(e.target.value)}
          disabled={isLoading}
          className="bg-background/50 backdrop-blur-sm"
        />
      </div>

      <Button
        type="submit"
        disabled={isLoading}
        className="w-full"
        size="lg"
      >
        <Search className="mr-2 h-5 w-5" />
        {isLoading ? 'Searching...' : 'Search Vehicles'}
      </Button>
    </form>
  );
};
