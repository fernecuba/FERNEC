import { BarChartEmotions } from "./BarChartEmotions";

export default function Results({ params }: { params: { data: string } }) {
  console.log("data:", params.data, atob(params.data));
  return (
    <main className="flex h-screen flex-col">
      <div className="container bg-gray-200 ">
        <h2 className="text-4xl font-bold p-4">
          Here <span className="text-green-700"> are </span>your
          <span className="text-green-700"> Results</span>
        </h2>
        <div className="pt-10 flex flex-row">
          <div className="w-1/2">
            <BarChartEmotions />
          </div>
          <div className="w-1/2 flex flex-col justify-around pl-14">
            <p className="font-bold">Your video has 60 seconds long</p>
            <p className="font-bold">
              for 20 seconds you looked{" "}
              <span className="text-green-600">happy</span>
            </p>
            <p className="font-bold">
              for 15 seconds you looked{" "}
              <span className="text-blue-300">neutral</span>
            </p>
            <p className="font-bold">
              for 10 seconds you looked{" "}
              <span className="text-yellow-600">surprised</span>
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
