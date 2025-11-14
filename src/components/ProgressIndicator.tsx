import { Progress } from '@/components/ui/progress';
import { Loader2 } from 'lucide-react';

interface ProgressIndicatorProps {
  current: number;
  total: number;
  currentSite: string;
  show: boolean;
}

export const ProgressIndicator = ({ current, total, currentSite, show }: ProgressIndicatorProps) => {
  if (!show) return null;

  const percentage = total > 0 ? (current / total) * 100 : 0;

  return (
    <div className="space-y-3 rounded-lg border bg-card p-6 shadow-sm">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Loader2 className="h-5 w-5 animate-spin text-primary" />
          <span className="font-medium">Searching vehicles...</span>
        </div>
        <span className="text-sm text-muted-foreground">
          {current} / {total} sites
        </span>
      </div>
      
      <Progress value={percentage} className="h-2" />
      
      <p className="text-sm text-muted-foreground">
        Currently scanning: <span className="font-medium text-foreground">{currentSite}</span>
      </p>
    </div>
  );
};
