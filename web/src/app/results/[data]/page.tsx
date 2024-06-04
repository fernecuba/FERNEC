import { BarChartEmotions } from "./BarChartEmotions";
import { DonutChartBinary } from "./DonutChartBinary";
import { TextInfo } from "./TextInfo";

interface EmotionResult {
  label:
    | "Neutral"
    | "Anger"
    | "Disgust"
    | "Fear"
    | "Happiness"
    | "Sadness"
    | "Surprise";
  total_frames: number;
}

interface BinaryEmotionResult {
  label: "Negative" | "Positive";
  total_frames: number;
}

export interface EmotionResults {
  total_frames: number;
  emotions: EmotionResult[];
  emotions_binary: BinaryEmotionResult[];
}

export default function Results({ params }: { params: { data: string } }) {
  const results = JSON.parse(
    atob(decodeURIComponent(params.data))
  ) as EmotionResults;

  return (
    <main className="flex h-screen flex-col">
      <div className="container bg-gray-200 ">
        <h2 className="text-4xl font-bold p-4">
          Here <span className="text-green-700"> are </span>your
          <span className="text-green-700"> Results</span>
        </h2>
        <section>
          <div className="pt-10 flex flex-row">
            <DonutChartBinary results={results} />
          </div>
        </section>
        <section>
          <div className="pt-10 flex flex-row">
            <div className="w-1/2">
              <BarChartEmotions results={results} />
            </div>
            <div className="w-1/2 flex flex-col justify-around items-center">
              <TextInfo results={results} />
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
