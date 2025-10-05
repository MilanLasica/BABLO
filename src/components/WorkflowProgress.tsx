import { useEffect, useState } from "react";
import { Loader2, Sparkles, CheckCircle2, Zap } from "lucide-react";

interface WorkflowProgressProps {
  isActive: boolean;
  onComplete: () => void;
}

const stages = [
  { id: 1, label: "Initializing", icon: Zap, duration: 1000 },
  { id: 2, label: "Processing", icon: Loader2, duration: 1500 },
  { id: 3, label: "Generating", icon: Sparkles, duration: 2000 },
  { id: 4, label: "Complete", icon: CheckCircle2, duration: 500 },
];

const WorkflowProgress = ({ isActive, onComplete }: WorkflowProgressProps) => {
  const [currentStage, setCurrentStage] = useState(0);

  useEffect(() => {
    if (!isActive) {
      setCurrentStage(0);
      return;
    }

    let timeoutId: NodeJS.Timeout;
    
    const advanceStage = (stageIndex: number) => {
      if (stageIndex < stages.length) {
        setCurrentStage(stageIndex);
        timeoutId = setTimeout(() => {
          if (stageIndex === stages.length - 1) {
            onComplete();
          } else {
            advanceStage(stageIndex + 1);
          }
        }, stages[stageIndex].duration);
      }
    };

    advanceStage(0);

    return () => {
      if (timeoutId) clearTimeout(timeoutId);
    };
  }, [isActive, onComplete]);

  if (!isActive) return null;

  return (
    <div className="space-y-6 animate-fade-in">
      {stages.map((stage, index) => {
        const Icon = stage.icon;
        const isActive = index === currentStage;
        const isComplete = index < currentStage;
        
        return (
          <div
            key={stage.id}
            className={`flex items-center gap-4 transition-all duration-500 ${
              isActive ? "scale-105" : "scale-100"
            } ${isComplete || isActive ? "opacity-100" : "opacity-40"}`}
          >
            <div
              className={`relative flex h-12 w-12 items-center justify-center rounded-full transition-all duration-500 ${
                isActive
                  ? "bg-gradient-to-br from-primary to-accent shadow-[0_0_30px_rgba(245,39,78,0.4)]"
                  : isComplete
                  ? "bg-primary"
                  : "bg-secondary"
              }`}
            >
              <Icon
                className={`h-6 w-6 text-primary-foreground ${
                  isActive && stage.id !== 4 ? "animate-spin" : ""
                }`}
              />
            </div>
            <div className="flex-1">
              <div
                className={`text-lg font-semibold transition-colors duration-300 ${
                  isActive ? "text-primary" : isComplete ? "text-foreground" : "text-muted-foreground"
                }`}
              >
                {stage.label}
              </div>
              {isActive && stage.id !== 4 && (
                <div className="mt-2 h-1 w-full overflow-hidden rounded-full bg-secondary">
                  <div className="h-full bg-gradient-to-r from-primary to-accent animate-pulse-glow" />
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default WorkflowProgress;
