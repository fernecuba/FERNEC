import { useState } from "react";
import { getQuestions } from "./action";

export default function Questions() {
  const [questions, setQuestions] = useState<string[]>([]);

  return (
    <div className="h-full flex flex-col">
      <button
        onClick={async () => {
          const { questions: q } = await getQuestions(
            "Messages during finals week."
          );

          setQuestions(q.questions);
        }}
      >
        Generar Preguntas
      </button>

      <div className="flex flex-col justify-center items-center  grow space-y-5">
        <p className="break-words p-0">{questions[0]}</p>
        <button className="border-2 rounded-md border-double p-2 border-slate-300">
          Next
        </button>
      </div>
    </div>
  );
}
