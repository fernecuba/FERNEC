"use client";
import {
  CardTitle,
  CardDescription,
  CardHeader,
  CardContent,
  CardFooter,
  Card,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import Image from "next/image";

export default function UploadVideo({
  setEmotionResult,
}: {
  setEmotionResult: (emotion: string) => void;
}) {
  const [submitFile, setSubmitFile] = useState<File>();

  const onSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!submitFile) return;

    let reader = new FileReader();
    reader.readAsDataURL(submitFile);
    reader.onload = async function () {
      // Split to remove data:image/png;base64
      // https://developer.mozilla.org/en-US/docs/Web/API/FileReader/result
      const image_base64 = (reader.result as string).split(",")[1];

      const response = await fetch("/api/predict/image", {
        method: "POST",
        body: JSON.stringify({
          image_base64,
        }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (response.ok) {
        const result = (await response.json()) as {
          emotion: string;
          predictions: number[];
        };
        setEmotionResult(result.emotion);
      } else {
        alert(`Failed ${await response.text()}`);
      }
    };
  };

  return (
    <Card className="flex flex-col">
      <CardHeader>
        <CardTitle>Upload Video</CardTitle>
        <CardDescription>
          Select a video from your device to upload.
        </CardDescription>
      </CardHeader>
      <form onSubmit={onSubmit}>
        <CardContent className="flex flex-1">
          <input
            id="pickImage"
            type="file"
            accept="image/png, image/jpeg"
            className="hidden"
            onChange={(e) => {
              if (e.target.files) {
                setSubmitFile(e.target.files[0]);
              }
            }}
          />
          <label
            htmlFor="pickImage"
            className="border-2 border-dashed border-gray-200/40 rounded-lg w-full flex items-center justify-center h-48 relative overflow-hidden"
          >
            {submitFile ? (
              <Image
                alt="bluerabbit ia studio logo"
                className="flex flex-1 object-cover"
                src={URL.createObjectURL(submitFile)}
                fill={true}
              />
            ) : (
              <svg
                className="w-16 h-16 text-gray-200"
                fill="none"
                height="64"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                width="64"
              >
                <polygon points="23 7 16 12 23 17 23 7 23 7" />
                <rect height="14" width="3" x="1" y="5" />
              </svg>
            )}
          </label>
        </CardContent>
        <CardFooter>
          <Button className="w-full mt-3" type="submit">
            Upload
          </Button>
        </CardFooter>
      </form>
    </Card>
  );
}
