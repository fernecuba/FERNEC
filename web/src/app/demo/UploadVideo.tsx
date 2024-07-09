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
import { cn } from "@/lib/utils";
import { uploadVideo } from "@/lib/actions";
import { useToast } from "@/components/ui/use-toast";
import ModalEnterMail from "./ModalEnterMail";

export default function UploadVideo({ className }: { className?: string }) {
  const [submitFile, setSubmitFile] = useState<File>();
  const [modal, openModal] = useState(false);
  const { toast } = useToast();

  const sendVideo = async (email: string) => {
    if (!submitFile) return;

    uploadVideo({
      email,
      video: submitFile,
      fileName: submitFile.name,
      fileType: submitFile.type,
    }).then((response) => {
      toast({
        description: response.ok ? "File upload" : "Error uploading file",
        variant: response.ok ? "default" : "destructive",
      });
    });
  };

  const onSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!submitFile) return;
    openModal(true);
  };

  return (
    <>
      <Card className={cn("flex flex-col", className)}>
        <CardHeader>
          <CardTitle>Upload Interview</CardTitle>
          <CardDescription>
            Select a video from your device to upload. Only MP4 files are
            accepted.
          </CardDescription>
        </CardHeader>
        <form onSubmit={onSubmit} className="flex-1 flex flex-col">
          <CardContent className="flex flex-1">
            <input
              id="pickImage"
              type="file"
              accept="video/mp4"
              className="hidden"
              onChange={(e) => {
                if (e.target.files) {
                  const file = e.target.files[0];
                  if (file.type !== "video/mp4") {
                    toast({
                      description:
                        "Only MP4 videos are accepted. Please select a valid file.",
                      variant: "destructive",
                    });
                    e.target.value = ""; // Clear the selected file
                  } else {
                    setSubmitFile(file);
                  }
                }
              }}
            />
            <label
              htmlFor="pickImage"
              className="border-2 border-dashed border-gray-200/40 rounded-lg w-full flex items-center justify-center relative overflow-hidden"
            >
              {submitFile ? (
                <video
                  className="object-fill absolute w-full h-full"
                  src={URL.createObjectURL(submitFile)}
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
            <Button className="w-full" type="submit">
              Upload
            </Button>
          </CardFooter>
        </form>
      </Card>
      <ModalEnterMail
        isOpen={modal}
        setIsOpen={openModal}
        action={(email) => sendVideo(email)}
      />
    </>
  );
}
