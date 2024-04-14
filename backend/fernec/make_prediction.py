from video_predictor import predict_video

def print_prediction(prediction):
    class_vocab = [
    "Neutral", "Anger", "Disgust", "Fear", "Happiness", "Sadness", "Surprise", "Other"
    ]
    print(class_vocab)
    for i, result in enumerate(prediction):
        result_argmax = result.argmax()
        result_label = class_vocab[result_argmax]
    
        # print(f"  {class_vocab[i]}: {probabilities[i] * 100:5.2f}%")
        print(f"frame {i} - result {result_label}")

prediction = predict_video("/home/eche/Documents/TPP/notebooks/Datasets/Aff-Wild2/raw-videos/358.mp4", "model4_rnn_poc3")
print_prediction(prediction)