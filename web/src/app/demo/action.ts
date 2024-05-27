"use server";
import { generateObject } from "ai";
import { google } from "@ai-sdk/google";
import { z } from "zod";

export async function getQuestions(input: string) {
  "use server";

  const { object: questions } = await generateObject({
    model: google("models/gemini-1.5-pro-latest"),
    system:
      "Sos un entrevistador para una empresa. Sos profesional y buscas evaluar la capacidad del entrevistado para ocupar el puesto.",
    prompt: `Desarrolla 4 preguntas para evaluar la capacidad del entrevistado en el campo del ${input}`,
    schema: z.object({
      questions: z.array(z.string().describe("Question for an interview")),
    }),
  });

  return { questions };
}
