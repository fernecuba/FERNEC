import { EmotionResults } from "./page";

export const TextInfo = ({ results }: { results: EmotionResults }) => {
  return (
    <>
      <p className="font-bold">
        Your video has {results.total_frames} frames long
      </p>
      <p className="font-bold">
        for{" "}
        {results.emotions.find((e) => e.label === "Happiness")?.total_frames}{" "}
        frames you looked <span className="text-green-600">happy</span>
      </p>
      <p className="font-bold">
        for {results.emotions.find((e) => e.label === "Neutral")?.total_frames}{" "}
        frames you looked <span className="text-blue-300">neutral</span>
      </p>
      <p className="font-bold">
        for {results.emotions.find((e) => e.label === "Surprise")?.total_frames}{" "}
        frames you looked <span className="text-yellow-600">surprised</span>
      </p>
    </>
  );
};
