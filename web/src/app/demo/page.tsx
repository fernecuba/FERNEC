import UploadVideo from "./UploadVideo";
import RecordVideo from "./RecordVideo";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function Demo() {
  return (
    <Tabs
      defaultValue="record"
      className="h-[calc(100vh-56px)] p-10 flex flex-col items-center"
    >
      <TabsList className="justify-self-center w-auto">
        <TabsTrigger value="record">Record</TabsTrigger>
        <TabsTrigger value="upload">Upload</TabsTrigger>
      </TabsList>
      <TabsContent
        value="record"
        className="bg-red-200 w-full h-full flex-1 flex-col"
      >
        <RecordVideo className="flex-1 h-full w-full bg-orange-200" />
      </TabsContent>
      <TabsContent
        value="upload"
        className="w-full h-full flex-1 flex-col bg-yellow-200"
      >
        <UploadVideo className="flex-1 h-full" />
      </TabsContent>
    </Tabs>
  );
}
