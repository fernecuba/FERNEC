import { useState } from "react";
import { ChevronRight, RotateCcw } from "lucide-react";
import { getQuestions } from "./action";

const fields = ["Data Analytics", "IT Support", "UX Design", "Cybersecurity"];

export default function Questions() {
  const [questions, setQuestions] = useState<string[]>([]);
  const [q_question, nextQuestion] = useState<number>(0);

  const fieldsItems = fields.map((field) => (
    <li
      key={field}
      className="bg-white p-2 rounded-md text-gray-500 flex flex-row justify-between hover:scale-105"
      onClick={async () => {
        const { questions: q } = await getQuestions(field);

        setQuestions(q.questions);
      }}
    >
      {field}
      <ChevronRight />
    </li>
  ));

  return (
    <div className="h-full flex flex-col">
      {questions.length === 0 ? (
        <>
          <h4 className="text-center p-2">
            What field do you want to practice for?
          </h4>
          <ul className="p-2 space-y-2">{fieldsItems}</ul>
        </>
      ) : (
        <div className="flex flex-col justify-center items-center grow space-y-5 relative">
          <RotateCcw
            className="absolute right-2 top-2"
            size={18}
            onClick={() => setQuestions([])}
          />
          <p className="break-words p-0 text-center">{questions[q_question]}</p>
          <button
            className="border-2 rounded-md border-double p-2 border-slate-300"
            onClick={() =>
              nextQuestion((index) => (index === 3 ? 0 : index + 1))
            }
          >
            Next
          </button>
        </div>
      )}
    </div>
  );

  /*
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
  );*/
}
