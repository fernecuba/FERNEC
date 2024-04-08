import {
  CardTitle,
  CardDescription,
  CardHeader,
  CardContent,
  CardFooter,
  Card,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function Component() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Upload Video</CardTitle>
        <CardDescription>
          Select a video from your device to upload.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="border-2 border-dashed border-gray-200/40 rounded-lg w-full p-6 flex items-center justify-center">
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
        </div>
      </CardContent>
      <CardFooter>
        <Button>Upload</Button>
      </CardFooter>
    </Card>
  );
}
