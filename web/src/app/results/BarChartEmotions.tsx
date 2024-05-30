"use client";
import { BarChart } from "@tremor/react";

["Anger", "Disgust", "Fear", "Happiness", "Neutral", "Sadness", "Surprise"];
const chartdata = [
  {
    name: "Anger",
    "Emotion %": 5,
  },
  {
    name: "Disgust",
    "Emotion %": 10,
  },
  {
    name: "Fear",
    "Emotion %": 5,
  },
  {
    name: "Happiness",
    "Emotion %": 20,
  },
  {
    name: "Neutral",
    "Emotion %": 40,
  },
  {
    name: "Sadness",
    "Emotion %": 10,
  },
  {
    name: "Surprise",
    "Emotion %": 10,
  },
];

const dataFormatter = (number: number) =>
  Intl.NumberFormat("us").format(number).toString();

export const BarChartEmotions = () => (
  <BarChart
    data={chartdata}
    index="name"
    categories={["Emotion %"]}
    colors={["blue"]}
    valueFormatter={dataFormatter}
    yAxisWidth={48}
    onValueChange={(v) => console.log(v)}
  />
);
