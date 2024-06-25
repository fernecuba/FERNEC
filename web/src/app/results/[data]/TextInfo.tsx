import { EmotionResults } from "./page";

export const TextInfo = ({ results }: { results: EmotionResults }) => {
  const emotionColors: { [key: string]: string } = {
    Neutral: "text-blue-300",
    Anger: "text-red-600",
    Disgust: "text-green-800",
    Fear: "text-purple-600",
    Happiness: "text-green-600",
    Sadness: "text-gray-600",
    Surprise: "text-yellow-600",
  };

  return (
    <>
      <p className="font-bold">
        Your video is {results.total_seconds} seconds long
      </p>
      {results.emotions.map((emotion) => (
        <p key={emotion.label} className="font-bold">
          for {emotion.total_seconds} seconds you looked{" "}
          <span className={emotionColors[emotion.label]}>
            {emotion.label.toLowerCase()}
          </span>
        </p>
      ))}
    </>
  );
};
