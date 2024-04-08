import UploadVideo from "@/components/video/UploadVideo";
import EmotionResults from "@/components/video/EmotionResults";

export default function Page() {
  return (
    <main className="flex min-h-screen flex-col items-center p-24 ">
      <div className="flex  w-full justify-center gap-x-6">
        <UploadVideo />
        <EmotionResults />
      </div>
    </main>
  );
}
