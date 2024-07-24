"use client";
import { BarChart } from "@tremor/react";
import { EmotionResults } from "./page";

const dataFormatter = (number: number) =>
  Intl.NumberFormat("us").format(number).toString();

export const BarChartEmotions = ({ results }: { results: EmotionResults }) => (
  <BarChart
    data={results.emotions.map((emotion) => ({
      name: emotion.label,
      "Emotion %": (emotion.total_seconds / results.total_seconds) * 100,
    }))}
    index="name"
    categories={["Emotion %"]}
    colors={["blue"]}
    valueFormatter={dataFormatter}
    yAxisWidth={48}
    onValueChange={(v) => console.log(v)}
    className="bg-white rounded-md drop-shadow-xl"
    showAnimation={true}
  />
);
