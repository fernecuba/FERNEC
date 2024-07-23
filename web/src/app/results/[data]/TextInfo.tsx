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

  const emotionDescriptions: { [key: string]: string } = {
    Neutral: "neutral",
    Anger: "angry",
    Disgust: "disgusted",
    Fear: "fearful",
    Happiness: "happy",
    Sadness: "sad",
    Surprise: "surprised",
  };

  // Sort emotions by total_seconds in descending order
  const sortedEmotions = results.emotions.sort((a, b) => b.total_seconds - a.total_seconds);

  return (
    <>
      <p className="font-bold">
      Total analysis: {results.total_seconds} seconds
      </p>
      {sortedEmotions.map((emotion) => (
        <p key={emotion.label} className="font-bold">
          for {emotion.total_seconds} seconds you looked{" "}
          <span className={emotionColors[emotion.label]}>
            {emotionDescriptions[emotion.label]}
          </span>
        </p>
      ))}
    </>
  );
};
