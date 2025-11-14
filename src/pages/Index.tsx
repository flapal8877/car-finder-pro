import { useState } from 'react';
import { Car } from 'lucide-react';
import { SearchForm } from '@/components/SearchForm';
import { ProgressIndicator } from '@/components/ProgressIndicator';
import { ResultsTable } from '@/components/ResultsTable';

import { Vehicle, SearchParams } from '@/types/vehicle';
import { searchVehicles } from '@/services/api';
import { useToast } from '@/hooks/use-toast';

const Index = () => {
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [progress, setProgress] = useState({ current: 0, total: 0, site: '' });
  const { toast } = useToast();

  const handleSearch = async (params: SearchParams) => {
    setIsSearching(true);
    setVehicles([]);
    setProgress({ current: 0, total: 0, site: '' });

    try {
      const results = await searchVehicles(
        params,
        (current, total, site) => {
          setProgress({ current, total, site });
        }
      );
      
      setVehicles(results);
      
      toast({
        title: 'Search Complete',
        description: `Found ${results.length} vehicle${results.length !== 1 ? 's' : ''} matching your criteria.`,
      });
    } catch (error) {
      toast({
        title: 'Search Failed',
        description: error instanceof Error ? error.message : 'An error occurred while searching.',
        variant: 'destructive',
      });
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[hsl(var(--gradient-start))] via-background to-[hsl(var(--gradient-end))]">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <div className="mb-8 text-center">
          <div className="inline-flex items-center gap-3 mb-4">
            <div className="p-3 bg-primary/10 rounded-xl">
              <Car className="h-8 w-8 text-primary" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              CarFinder Pro
            </h1>
          </div>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            Real-time private-party vehicle sourcing from 35+ marketplaces.
            Find the best deals instantly.
          </p>
        </div>

        

        {/* Main Content */}
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Search Form */}
          <div className="lg:col-span-1">
            <div className="bg-card/80 backdrop-blur-sm rounded-xl border shadow-lg p-6 sticky top-8">
              <h2 className="text-xl font-semibold mb-6">Search Parameters</h2>
              <SearchForm onSearch={handleSearch} isLoading={isSearching} />
            </div>
          </div>

          {/* Results Area */}
          <div className="lg:col-span-2 space-y-6">
            <ProgressIndicator
              current={progress.current}
              total={progress.total}
              currentSite={progress.site}
              show={isSearching}
            />
            
            <ResultsTable vehicles={vehicles} />
            
            {!isSearching && vehicles.length === 0 && (
              <div className="text-center py-12 bg-card/50 backdrop-blur-sm rounded-xl border">
                <Car className="h-16 w-16 mx-auto text-muted-foreground mb-4" />
                <h3 className="text-xl font-semibold mb-2">Ready to Find Vehicles</h3>
                <p className="text-muted-foreground">
                  Enter your search criteria to start finding the best private-party deals.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
