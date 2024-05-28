export const uploadVideo = ({
  video,
  fileName,
  fileType,
}: {
  video: Blob;
  fileName: string;
  fileType: string;
}) => {
  // Upload the blob to a back-end
  const formData = new FormData();

  formData.append("video_file", video, `${fileName}.${fileType}`);
  return fetch("http://localhost:8000/predict/video", {
    method: "POST",
    body: formData,
  });
};
