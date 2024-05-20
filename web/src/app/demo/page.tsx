import UploadVideo from "./UploadVideo";
import RecordVideoCard from "./RecordVideoCard";

export default function Demo() {
  return (
    <main className="flex min-h-screen flex-col items-center p-24 ">
      <div className="flex w-full justify-center gap-6 flex-wrap">
        <UploadVideo className="w-[400px] h-[500px]" />
        <RecordVideoCard className="w-[400px] flex-initial" />
      </div>
    </main>
  );
}
