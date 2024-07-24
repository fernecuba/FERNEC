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
  total_seconds: number;
  total_sequences: number;
}

interface BinaryEmotionResult {
  label: "Negative" | "Positive";
  total_frames: number;
  total_seconds: number;
  total_sequences: number;
}

export interface EmotionResults {
  total_frames: number;
  total_seconds: number;
  real_total_seconds: number;
  fps: number;
  emotions: EmotionResult[];
  emotions_binary: BinaryEmotionResult[];
}

function filterEmotionResults(results: EmotionResults): EmotionResults {
  const filteredResults = results.emotions.filter(
    (emotion) => emotion.total_seconds > 0
  );

  return {
    ...results,
    emotions: filteredResults,
  };
}

export default function Results({ params }: { params: { data: string } }) {
  const results = JSON.parse(
    atob(decodeURIComponent(params.data))
  ) as EmotionResults;

  // Filtrar los resultados donde total_sequences es distinto de 0
  const nonZeroSequencesResults = filterEmotionResults(results);

  return (
    <main className="flex h-screen flex-col">
      <div className="container bg-gray-200 rounded-md drop-shadow-2xl">
        <h2 className="text-4xl font-bold p-4 drop-shadow-xl">
          Here <span className="text-green-700"> are </span>your
          <span className="text-green-700"> Results</span>
        </h2>
        <section>
          <div className="pt-10 flex flex-row">
            <DonutChartBinary results={results} />
          </div>
        </section>
        <section>
          <div className="py-10 flex flex-row">
            <div className="w-1/2">
              <BarChartEmotions results={results} />
            </div>
            <div className="w-1/2 flex flex-col justify-around items-center">
              <TextInfo results={nonZeroSequencesResults} />
            </div>
          </div>
        </section>
      </div>
      <div className="w-full flex justify-center items-end mt-4 mb-4">
        <p className="text-md text-gray-600">
          The presented results are based on automated analysis and may not be
          entirely accurate.
        </p>
      </div>
    </main>
  );
}
