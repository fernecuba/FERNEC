"use client";
import { useRecordWebcam } from "react-record-webcam";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";

const RecordingPulse = ({ className }: { className?: string }) => (
  <span className={cn("relative flex h-4 w-4", className)}>
    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-600 opacity-75"></span>
    <span className="relative inline-flex rounded-full h-4 w-4 bg-red-600"></span>
  </span>
);

export default function Record() {
  const {
    createRecording,
    openCamera,
    startRecording,
    stopRecording,
    download,
    activeRecordings,
  } = useRecordWebcam();

  const recordVideo = async () => {
    const recording = (await createRecording()) as Awaited<
      ReturnType<typeof createRecording>
    >;
    if (!recording) return;
    await openCamera(recording.id);
    await startRecording(recording.id);
    //await new Promise((resolve) => setTimeout(resolve, 3000)); // Record for 3 seconds
  };

  const stop = async (recordingId: string) => {
    await stopRecording(recordingId);
    //await download(recording.id); // Download the recording
  };

  const recording = activeRecordings.at(-1);

  return (
    <main className="flex h-screen flex-col p-24">
      <div className="h-3/4 container flex flex-row p-0 space-x-2">
        <div className="w-3/4 h-full flex flex-col border-2 bg-gray-200 rounded-lg">
          {recording?.id ? (
            <div className="flex flex-1 relative" key={recording.id}>
              {recording.status === "RECORDING" && (
                <RecordingPulse className="absolute top-2 left-2" />
              )}
              <video
                className="rounded-lg"
                ref={recording.webcamRef}
                autoPlay
              />
              {/*<video ref={recording.previewRef} autoPlay loop />*/}
            </div>
          ) : (
            <Skeleton className="flex flex-1 bg-gray-300" />
          )}
          <div className="flex flex-row justify-evenly py-2">
            <Button
              className="bg-green-500"
              onClick={recordVideo}
              disabled={recording?.status === "RECORDING"}
            >
              Start Recording
            </Button>

            {recording ? (
              <Button className="bg-red-500" onClick={() => stop(recording.id)}>
                Stop Recording
              </Button>
            ) : (
              <Button className="bg-red-500" disabled={true}>
                Stop Recording
              </Button>
            )}
          </div>
        </div>
        <div className="flex-1 border-2 rounded-lg bg-gray-200 gap-2">
          {activeRecordings.map((recording) => (
            <div className="h-1/3 w-full rounded-lg" key={recording.id}>
              <video
                className="rounded-lg"
                ref={recording.previewRef}
                loop
                autoPlay
              />
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
