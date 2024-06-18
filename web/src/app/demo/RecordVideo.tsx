"use client";
import { useRecordWebcam } from "react-record-webcam";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useEffect, useState } from "react";
import { Trash2, FileUp, Volume2Icon, VolumeX } from "lucide-react";
import { useToast } from "@/components/ui/use-toast";
import { uploadVideo } from "@/lib/actions";
import Questions from "./Questions";
import ModalEnterMail from "./ModalEnterMail";

const RecordingPulse = ({ className }: { className?: string }) => (
  <span className={cn("relative flex h-4 w-4", className)}>
    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-600 opacity-75"></span>
    <span className="relative inline-flex rounded-full h-4 w-4 bg-red-600"></span>
  </span>
);

export default function RecordVideo({ className }: { className?: string }) {
  const {
    createRecording,
    openCamera,
    closeCamera,
    startRecording,
    stopRecording,
    download,
    activeRecordings,
    clearPreview,
  } = useRecordWebcam();
  const { toast } = useToast();
  const [modal, openModal] = useState(false);
  const [isMute, mute] = useState(false);

  const initCamera = async () => {
    createRecording().then((recording) => {
      if (recording) openCamera(recording.id);
    });
  };

  const start = async (recordingId: string) => {
    /*
    const recording = (await createRecording()) as Awaited<
      ReturnType<typeof createRecording>
    >;
    */
    await startRecording(recordingId);
  };

  const stop = async (recordingId: string) => {
    await stopRecording(recordingId);
  };

  const upload = async (
    recorded: Awaited<ReturnType<typeof createRecording>>,
    email: string
  ) => {
    if (!recorded?.blob) {
      alert("No video to upload");
      return;
    }

    const response = await uploadVideo({
      email,
      video: recorded.blob,
      fileName: recorded.fileName,
      fileType: recorded.fileType,
    });

    toast({
      description: response.ok ? "File upload" : "Error uploading file",
      variant: response.ok ? "default" : "destructive",
    });
  };

  const recording = activeRecordings.at(-1);

  useEffect(() => {
    initCamera();
  }, []);

  if (!recording) return null;

  return (
    <>
      <main className={cn("flex flex-col", className)}>
        <div className="h-full flex flex-row p-0 space-x-2">
          <div className="w-3/4 h-full flex flex-col border-2 bg-gray-200 rounded-lg">
            <div className="flex flex-1 relative" key={recording.id}>
              {recording.status === "RECORDING" && (
                <RecordingPulse className="absolute top-2 left-2 z-10" />
              )}
              {recording.status === "STOPPED" && isMute && (
                <VolumeX
                  className="absolute top-2 z-10 right-2"
                  color="white"
                  onClick={() => mute((m) => !m)}
                  size={30}
                />
              )}
              {recording.status === "STOPPED" && !isMute && (
                <Volume2Icon
                  className="absolute top-2 z-10 right-2"
                  color="white"
                  onClick={() => mute((m) => !m)}
                  size={30}
                />
              )}
              <video
                className={cn(
                  "rounded-lg absolute w-full h-full object-fill",
                  recording.status === "OPEN" ||
                    recording.status === "RECORDING" ||
                    recording.status === "INITIAL"
                    ? "block"
                    : "hidden"
                )}
                ref={recording.webcamRef}
                autoPlay
              />
              <video
                className={cn(
                  "rounded-lg absolute w-full h-full object-fill",
                  recording.status === "STOPPED" ? "block" : "hidden"
                )}
                ref={recording.previewRef}
                muted={isMute}
                autoPlay
                loop
              />
              {/*<video ref={recording.previewRef} autoPlay loop />*/}
            </div>

            <div className="flex flex-row justify-evenly py-2">
              {recording.status === "OPEN" ||
              recording.status === "RECORDING" ||
              recording.status === "INITIAL" ? (
                <>
                  <Button
                    className="bg-green-500"
                    onClick={() => start(recording.id)}
                    disabled={recording?.status === "RECORDING"}
                  >
                    Start Recording
                  </Button>

                  <Button
                    className="bg-red-500"
                    onClick={() => stop(recording.id)}
                  >
                    Stop Recording
                  </Button>
                </>
              ) : (
                <>
                  <FileUp
                    size={40}
                    color="green"
                    onClick={() => openModal(true)}
                  />
                  <Trash2
                    size={40}
                    color="red"
                    onClick={() => clearPreview(recording.id)}
                  />
                </>
              )}
            </div>
          </div>
          <div className="flex-1 border-2 rounded-lg bg-gray-200 gap-2">
            <Questions />
          </div>
        </div>
      </main>
      <ModalEnterMail
        isOpen={modal}
        setIsOpen={openModal}
        action={(email) => upload(recording, email)}
      />
    </>
  );
}
