import { CardTitle, CardHeader, CardContent, Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

export default function EmotionResults() {
  return (
    <Card className="w-full max-w-lg">
      <CardHeader>
        <CardTitle>Emotion Detection Results</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <div className="flex items-center gap-4">
          <div className="w-16 h-9 rounded-lg overflow-hidden">
            <img
              alt="Video thumbnail"
              className="aspect-video object-cover rounded-lg"
              height={18}
              src="/placeholder.svg"
              width={32}
            />
          </div>
          <ul className="grid gap-1">
            <li>Happy</li>
            <li>Sad</li>
            <li>Angry</li>
            <li>Surprised</li>
            <li>Neutral</li>
          </ul>
          <ul className="grid gap-1 text-right">
            <li>70%</li>
            <li>10%</li>
            <li>5%</li>
            <li>10%</li>
            <li>5%</li>
          </ul>
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
      </CardContent>
    </Card>
  );
}
