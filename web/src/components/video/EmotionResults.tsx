import { CardTitle, CardHeader, CardContent, Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

export default function EmotionResults({ emotion }: { emotion?: string }) {
  return (
    <Card className="w-full max-w-lg">
      <CardHeader>
        <CardTitle>Emotion Detection Results</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        {emotion ? (
          <>
            <div className="flex items-center gap-4">
              <h3>Prediction: {emotion}</h3>
            </div>
            <div className="grid gap-2.5">
              <div className="flex items-center gap-2.5">
                <span className="w-16 text-sm">Happy</span>
                <Progress className="w-full" value={70} />
              </div>
              <div className="flex items-center gap-2.5">
                <span className="w-16 text-sm">Sad</span>
                <Progress className="w-full" value={10} />
              </div>
              <div className="flex items-center gap-2.5">
                <span className="w-16 text-sm">Angry</span>
                <Progress className="w-full" value={5} />
              </div>
              <div className="flex items-center gap-2.5">
                <span className="w-16 text-sm">Surprised</span>
                <Progress className="w-full" value={10} />
              </div>
              <div className="flex items-center gap-2.5">
                <span className="w-16 text-sm">Neutral</span>
                <Progress className="w-full" value={5} />
              </div>
            </div>
          </>
        ) : (
          <div className="flex items-center gap-4">
            Upload video for predictions
          </div>
        )}
      </CardContent>
    </Card>
  );
}
