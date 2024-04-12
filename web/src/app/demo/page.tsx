"use client";
import UploadVideo from "@/components/video/UploadVideo";
import EmotionResults from "@/components/video/EmotionResults";
import { useState } from "react";

export default function Page() {
  const [emotion, setEmotion] = useState<string>();

  return (
    <main className="flex min-h-screen flex-col items-center p-24 ">
      <div className="flex  w-full justify-center gap-x-6">
        <UploadVideo setEmotionResult={setEmotion} />
        <EmotionResults emotion={emotion} />
      </div>
    </main>
  );
}
