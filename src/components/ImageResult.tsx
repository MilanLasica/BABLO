interface ImageResultProps {
  imageUrl: string | null;
  isVisible: boolean;
}

const ImageResult = ({ imageUrl, isVisible }: ImageResultProps) => {
  if (!isVisible || !imageUrl) return null;

  // Check if the URL is a video file
  const isVideo = imageUrl.match(/\.(mp4|webm|ogg|mov)(\?|$)/i);

  return (
    <div className="animate-scale-in">
      <div className="overflow-hidden rounded-2xl border border-border bg-card shadow-[var(--shadow-card)]">
        {isVideo ? (
          <video
            src={imageUrl}
            controls
            autoPlay
            loop
            muted
            className="h-auto w-full object-cover"
          >
            Your browser does not support the video tag.
          </video>
        ) : (
          <img
            src={imageUrl}
            alt="Generated result"
            className="h-auto w-full object-cover transition-transform duration-500 hover:scale-105"
          />
        )}
      </div>
      <p className="mt-4 text-center text-sm text-muted-foreground animate-fade-in">
        Your {isVideo ? 'video' : 'image'} is ready! 🎉
      </p>
    </div>
  );
};

export default ImageResult;
