"use server";
import { generateObject } from "ai";
import { google } from "@ai-sdk/google";
import { z } from "zod";

export async function getQuestions(input: string) {
  "use server";

  const { object: questions } = await generateObject({
    model: google("models/gemini-1.5-pro-latest"),
    system:
      "You are an interviewer for a company. You are professional and seek to evaluate the interviewee's ability to fill the position.",
    prompt: `Develop 4 questions to evaluate the ability of the interviewee in the field of ${input}`,
    schema: z.object({
      questions: z.array(z.string().describe("Question for an interview")),
    }),
  });

  return { questions };
}
