import { AlertCircle, Settings } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

export const ApiConfigBanner = () => {
  const [apiUrl, setApiUrl] = useState(
    localStorage.getItem('railway_api_url') || ''
  );
  const [isOpen, setIsOpen] = useState(false);

  const hasApiUrl = import.meta.env.VITE_RAILWAY_API_URL || apiUrl;

  const handleSave = () => {
    localStorage.setItem('railway_api_url', apiUrl);
    setIsOpen(false);
    window.location.reload();
  };

  if (hasApiUrl) return null;

  return (
    <Alert variant="destructive" className="mb-6">
      <AlertCircle className="h-4 w-4" />
      <AlertTitle>Railway API Not Configured</AlertTitle>
      <AlertDescription className="mt-2 flex items-center justify-between">
        <span>Please configure your Railway backend URL to start searching.</span>
        <Dialog open={isOpen} onOpenChange={setIsOpen}>
          <DialogTrigger asChild>
            <Button variant="outline" size="sm">
              <Settings className="mr-2 h-4 w-4" />
              Configure
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Configure Railway Backend</DialogTitle>
              <DialogDescription>
                Enter your Railway backend URL (e.g., https://your-app.railway.app)
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <Label htmlFor="apiUrl">Railway API URL</Label>
                <Input
                  id="apiUrl"
                  placeholder="https://your-app.railway.app"
                  value={apiUrl}
                  onChange={(e) => setApiUrl(e.target.value)}
                />
              </div>
              <Button onClick={handleSave} className="w-full">
                Save Configuration
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </AlertDescription>
    </Alert>
  );
};
