"use server";
import { generateObject } from "ai";
import { google } from "@ai-sdk/google";
import { z } from "zod";

export async function getQuestions(input: string) {
  "use server";

  const { object: questions } = await generateObject({
    model: google("models/gemini-1.5-pro-latest"),
    system:
      "Sos un entrevistador para una empresa. Sos profesional y buscas lo mejor tanto para la empresa como para el entrevistado.",
    prompt:
      "Genera 4 preguntas para evaluar la capacidad del entrevistado en el campo del desarrollo Front-end",
    schema: z.object({
      questions: z.array(z.string().describe("Question for an interview")),
    }),
  });

  return { questions };
}
