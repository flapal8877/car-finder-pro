import { useState } from 'react';
import { Search, ChevronDown } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { Checkbox } from '@/components/ui/checkbox';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { SearchParams } from '@/types/vehicle';

interface SearchFormProps {
  onSearch: (params: SearchParams) => void;
  isLoading: boolean;
}

const VEHICLE_MAKES = [
  'Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW', 'Mercedes-Benz', 'Audi', 'Tesla', 
  'Nissan', 'Mazda', 'Subaru', 'Volkswagen', 'Hyundai', 'Kia', 'Lexus', 'Acura',
  'GMC', 'RAM', 'Dodge', 'Jeep', 'Porsche', 'Land Rover', 'Volvo', 'Jaguar',
  'Infiniti', 'Cadillac', 'Buick', 'Lincoln', 'Genesis', 'Alfa Romeo'
];

const BODY_STYLES = ['Sedan', 'SUV', 'Truck', 'Coupe', 'Van', 'Convertible', 'Wagon', 'Hatchback'];
const FUEL_TYPES = ['Gas', 'Hybrid', 'Plug-in Hybrid', 'Electric', 'Diesel'];
const CONDITIONS = ['Any', 'Excellent', 'Good', 'Fair'];

export const SearchForm = ({ onSearch, isLoading }: SearchFormProps) => {
  const [keyword, setKeyword] = useState('');
  const [location, setLocation] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  
  // Advanced filters
  const [make, setMake] = useState('');
  const [model, setModel] = useState('');
  const [minYear, setMinYear] = useState('');
  const [maxYear, setMaxYear] = useState('');
  const [maxMileage, setMaxMileage] = useState('');
  const [zipCode, setZipCode] = useState('');
  const [radius, setRadius] = useState([50]);
  const [bodyStyles, setBodyStyles] = useState<string[]>([]);
  const [condition, setCondition] = useState('Any');
  const [fuelTypes, setFuelTypes] = useState<string[]>([]);
  const [privateOnly, setPrivateOnly] = useState(false);
  const [searchMode, setSearchMode] = useState<'fast' | 'full'>('fast');

  const handleBodyStyleToggle = (style: string) => {
    setBodyStyles(prev => 
      prev.includes(style) ? prev.filter(s => s !== style) : [...prev, style]
    );
  };

  const handleFuelTypeToggle = (type: string) => {
    setFuelTypes(prev => 
      prev.includes(type) ? prev.filter(t => t !== type) : [...prev, type]
    );
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch({
      keyword: keyword.trim(),
      location: location.trim(),
      maxPrice: parseInt(maxPrice) || 999999,
      make: make || undefined,
      model: model.trim() || undefined,
      minYear: minYear ? parseInt(minYear) : undefined,
      maxYear: maxYear ? parseInt(maxYear) : undefined,
      maxMileage: maxMileage ? parseInt(maxMileage) : undefined,
      zipCode: zipCode.trim() || undefined,
      radius: radius[0],
      bodyStyles: bodyStyles.length > 0 ? bodyStyles : undefined,
      condition: condition !== 'Any' ? condition : undefined,
      fuelTypes: fuelTypes.length > 0 ? fuelTypes : undefined,
      privateOnly,
      searchMode,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Basic Search */}
      <div className="space-y-4">
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
      </div>

      {/* Advanced Filters */}
      <Accordion type="single" collapsible className="border rounded-lg">
        <AccordionItem value="advanced" className="border-0">
          <AccordionTrigger className="px-4 hover:no-underline">
            <div className="flex items-center gap-2">
              <ChevronDown className="h-4 w-4" />
              <span className="font-medium">Advanced Filters</span>
            </div>
          </AccordionTrigger>
          <AccordionContent className="px-4 pb-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-4">
              {/* Vehicle Details */}
              <div className="space-y-2">
                <Label htmlFor="make">Make</Label>
                <Select value={make} onValueChange={setMake} disabled={isLoading}>
                  <SelectTrigger className="bg-background/50">
                    <SelectValue placeholder="Any Make" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="">Any Make</SelectItem>
                    {VEHICLE_MAKES.map(m => (
                      <SelectItem key={m} value={m}>{m}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="model">Model</Label>
                <Input
                  id="model"
                  type="text"
                  placeholder="e.g., Civic"
                  value={model}
                  onChange={(e) => setModel(e.target.value)}
                  disabled={isLoading}
                  className="bg-background/50 backdrop-blur-sm"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="minYear">Min Year</Label>
                <Input
                  id="minYear"
                  type="number"
                  placeholder="2000"
                  min="1980"
                  max="2025"
                  value={minYear}
                  onChange={(e) => setMinYear(e.target.value)}
                  disabled={isLoading}
                  className="bg-background/50 backdrop-blur-sm"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="maxYear">Max Year</Label>
                <Input
                  id="maxYear"
                  type="number"
                  placeholder="2025"
                  min="1980"
                  max="2025"
                  value={maxYear}
                  onChange={(e) => setMaxYear(e.target.value)}
                  disabled={isLoading}
                  className="bg-background/50 backdrop-blur-sm"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="maxMileage">Max Mileage</Label>
                <Input
                  id="maxMileage"
                  type="number"
                  placeholder="100000"
                  value={maxMileage}
                  onChange={(e) => setMaxMileage(e.target.value)}
                  disabled={isLoading}
                  className="bg-background/50 backdrop-blur-sm"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="zipCode">ZIP Code</Label>
                <Input
                  id="zipCode"
                  type="text"
                  placeholder="90210"
                  maxLength={5}
                  value={zipCode}
                  onChange={(e) => setZipCode(e.target.value)}
                  disabled={isLoading}
                  className="bg-background/50 backdrop-blur-sm"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="radius">Search Radius: {radius[0]} miles</Label>
                <Slider
                  id="radius"
                  min={10}
                  max={200}
                  step={10}
                  value={radius}
                  onValueChange={setRadius}
                  disabled={isLoading}
                  className="mt-2"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="condition">Condition</Label>
                <Select value={condition} onValueChange={setCondition} disabled={isLoading}>
                  <SelectTrigger className="bg-background/50">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {CONDITIONS.map(c => (
                      <SelectItem key={c} value={c}>{c}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Body Styles */}
            <div className="space-y-3 mt-4">
              <Label>Body Styles</Label>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {BODY_STYLES.map(style => (
                  <div key={style} className="flex items-center space-x-2">
                    <Checkbox
                      id={`body-${style}`}
                      checked={bodyStyles.includes(style)}
                      onCheckedChange={() => handleBodyStyleToggle(style)}
                      disabled={isLoading}
                    />
                    <Label htmlFor={`body-${style}`} className="text-sm font-normal cursor-pointer">
                      {style}
                    </Label>
                  </div>
                ))}
              </div>
            </div>

            {/* Fuel Types */}
            <div className="space-y-3 mt-4">
              <Label>Fuel Types</Label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {FUEL_TYPES.map(type => (
                  <div key={type} className="flex items-center space-x-2">
                    <Checkbox
                      id={`fuel-${type}`}
                      checked={fuelTypes.includes(type)}
                      onCheckedChange={() => handleFuelTypeToggle(type)}
                      disabled={isLoading}
                    />
                    <Label htmlFor={`fuel-${type}`} className="text-sm font-normal cursor-pointer">
                      {type}
                    </Label>
                  </div>
                ))}
              </div>
            </div>

            {/* Preferences */}
            <div className="space-y-4 mt-4">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="privateOnly"
                  checked={privateOnly}
                  onCheckedChange={(checked) => setPrivateOnly(checked as boolean)}
                  disabled={isLoading}
                />
                <Label htmlFor="privateOnly" className="font-normal cursor-pointer">
                  Private Sellers Only (No Dealers)
                </Label>
              </div>

              <div className="space-y-2">
                <Label>Search Mode</Label>
                <RadioGroup value={searchMode} onValueChange={(v) => setSearchMode(v as 'fast' | 'full')} disabled={isLoading}>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="fast" id="fast" />
                    <Label htmlFor="fast" className="font-normal cursor-pointer">
                      Fast (10 sites, ~30 seconds)
                    </Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="full" id="full" />
                    <Label htmlFor="full" className="font-normal cursor-pointer">
                      Full (35+ sites, ~2 minutes)
                    </Label>
                  </div>
                </RadioGroup>
              </div>
            </div>
          </AccordionContent>
        </AccordionItem>
      </Accordion>

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
