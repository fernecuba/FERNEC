"use client";
import { Card, DonutChart, List, ListItem } from "@tremor/react";
import { cn } from "@/lib/utils";
import { EmotionResults } from "./page";

export const DonutChartBinary = ({ results }: { results: EmotionResults }) => {
  const data = results.emotions_binary.map((emotion) => ({
    name: emotion.label,
    amount: emotion.total_seconds,
    share: `${(
      (emotion.total_seconds / results.total_seconds) * 100
    ).toFixed(1)}%`,
    color: emotion.label === "Negative" ? "bg-red-500" : "bg-green-500",
  }));
  return (
    <Card className="sm:mx-auto sm:max-w-lg">
      <DonutChart
        className="mt-8"
        data={data}
        category="amount"
        index="name"
        valueFormatter={(value: number) =>
          Intl.NumberFormat("us").format(value).toString()
        }
        showTooltip={true}
        colors={["red", "green"]}
      />
      <p className="mt-8 flex items-center justify-between text-tremor-label text-tremor-content dark:text-dark-tremor-content">
        <span>Category</span>
        <span>Amount</span>
      </p>
      <List className="mt-2">
        {data.map((item) => (
          <ListItem key={item.name} className="space-x-6">
            <div className="flex items-center space-x-2.5 truncate">
              <span
                className={cn(item.color, "h-2.5 w-2.5 shrink-0 rounded-sm")}
                aria-hidden={true}
              />
              <span className="truncate dark:text-dark-tremor-content-emphasis">
                {item.name}
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="rounded-tremor-small bg-tremor-background-subtle px-1.5 py-0.5 text-tremor-label font-medium tabular-nums text-tremor-content-emphasis dark:bg-dark-tremor-background-subtle dark:text-dark-tremor-content-emphasis">
                {item.share}
              </span>
            </div>
          </ListItem>
        ))}
      </List>
    </Card>
  );
};
