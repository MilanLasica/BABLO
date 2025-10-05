import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import WorkflowProgress from "@/components/WorkflowProgress";
import ImageResult from "@/components/ImageResult";
import { Play } from "lucide-react";
import { triggerN8nWorkflow } from "@/services/n8n";
import { useToast } from "@/hooks/use-toast";

const Index = () => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [showResult, setShowResult] = useState(false);
  const [prompt, setPrompt] = useState("");
  const [negativePrompt, setNegativePrompt] = useState("");
  const { toast } = useToast();

  const handleStartWorkflow = async () => {
    if (!prompt.trim()) {
      toast({
        title: "Prompt required",
        description: "Please enter a prompt for your video",
        variant: "destructive",
      });
      return;
    }

    setIsProcessing(true);
    setShowResult(false);
    setImageUrl(null);

    try {
      // Call the Modal workflow with ComfyUI
      const response = await triggerN8nWorkflow({
        prompt: prompt.trim(),
        negative_prompt: negativePrompt.trim() || undefined,
        timestamp: new Date().toISOString(),
      });

      if (response.success) {
        toast({
          title: "Workflow completed",
          description: response.message || "Your workflow has finished successfully",
        });

        // Set the image URL from the workflow response
        if (response.imageUrl) {
          setImageUrl(response.imageUrl);
        } else {
          // Fallback to placeholder if no image URL returned
          setImageUrl("https://images.unsplash.com/photo-1618005198919-d3d4b5a92ead?w=800&h=600&fit=crop");
        }

        setShowResult(true);
      }
    } catch (error) {
      console.error("Workflow error:", error);
      toast({
        title: "Workflow failed",
        description: error instanceof Error ? error.message : "Failed to execute workflow",
        variant: "destructive",
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const handleWorkflowComplete = () => {
    // This is called when the progress animation completes
    // The actual workflow is already done at this point
  };

  return (
    <div className="min-h-screen bg-[var(--gradient-subtle)]">
      <div className="container mx-auto px-4 py-12">
        <div className="mx-auto max-w-2xl">
          {/* Header */}
          <div className="mb-12 text-center animate-fade-in">
            <h1 className="mb-4 bg-gradient-to-r from-primary to-accent bg-clip-text text-5xl font-bold text-transparent">
              Balbo
            </h1>
            <p className="text-2xl font-semibold mb-2 text-foreground">
              Desire on Demand
            </p>
            <p className="text-lg text-muted-foreground">
              AI-powered video generation
            </p>
          </div>

          {/* Main Card */}
          <div className="rounded-3xl border border-border bg-card p-8 shadow-[var(--shadow-card)] backdrop-blur-sm">
            {!isProcessing && !showResult && (
              <div className="space-y-6 animate-slide-up">
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="prompt" className="text-lg font-semibold">
                      What should happen in the video?
                    </Label>
                    <Textarea
                      id="prompt"
                      placeholder="e.g., A cat walking on the beach at sunset, waves crashing gently..."
                      value={prompt}
                      onChange={(e) => setPrompt(e.target.value)}
                      className="min-h-[120px] resize-none"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="negative-prompt" className="text-sm font-medium text-muted-foreground">
                      Negative Prompt (Optional)
                    </Label>
                    <Textarea
                      id="negative-prompt"
                      placeholder="What to avoid in the video..."
                      value={negativePrompt}
                      onChange={(e) => setNegativePrompt(e.target.value)}
                      className="min-h-[80px] resize-none"
                    />
                  </div>
                </div>

                <div className="flex justify-center pt-4">
                  <Button
                    onClick={handleStartWorkflow}
                    size="lg"
                    className="bg-gradient-to-r from-primary to-accent hover:opacity-90 transition-all duration-300 shadow-[var(--shadow-glow)] hover:shadow-[0_0_50px_rgba(245,39,78,0.35)] text-primary-foreground px-8 py-6 text-lg"
                  >
                    <Play className="mr-2 h-5 w-5" />
                    Generate Video
                  </Button>
                </div>
              </div>
            )}

            {isProcessing && (
              <WorkflowProgress
                isActive={isProcessing}
                onComplete={handleWorkflowComplete}
              />
            )}

            {showResult && (
              <div className="space-y-6">
                <ImageResult imageUrl={imageUrl} isVisible={showResult} />
                <div className="flex justify-center">
                  <Button
                    onClick={handleStartWorkflow}
                    variant="outline"
                    size="lg"
                    className="transition-all duration-300 hover:border-primary hover:text-primary"
                  >
                    <Play className="mr-2 h-5 w-5" />
                    Run Again
                  </Button>
                </div>
              </div>
            )}
          </div>

          {/* Footer Note */}
          <div className="mt-8 text-center text-sm text-muted-foreground animate-fade-in">
            <p>Powered by AI • Payments via Aeternity blockchain</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
