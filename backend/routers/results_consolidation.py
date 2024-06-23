import os
import numpy as np
from loguru import logger

from preprocessing.frames_generator.strategy.videos_processor.videos import frames_to_seconds

NEGATIVE_EMOTIONS = ["Anger", "Disgust", "Fear", "Sadness", "Surprise"]
POSITIVE_EMOTIONS = ["Neutral", "Happiness"]


def consolidate_results(predictions, predictions_binary, frames_amount, fps, video_config, binary_acceptance_threshold):
    class_vocab_emotions = ["Neutral", "Anger", "Disgust", "Fear", "Happiness", "Sadness", "Surprise"]
    class_vocab_binary = ["Negative", "Positive"]

    emotions_list = calculate_emotion_counts(predictions, class_vocab_emotions, frames_amount, fps, video_config)
    emotions_list_binary = calculate_emotion_counts(predictions_binary, class_vocab_binary, frames_amount, fps,
                                                    video_config)

    # Total frames
    total_frames = sum([emotion["total_frames"] for emotion in emotions_list])
    total_frames_binary = sum([emotion["total_frames"] for emotion in emotions_list_binary])

    raw_result = {
        "total_frames": total_frames,
        "total_seconds": frames_to_seconds(total_frames, fps),
        "fps": fps,
        "emotions": emotions_list,
        "emotions_binary": emotions_list_binary
    }

    logger.success(f"raw_result is: {raw_result}")

    # Calculate percentages
    percentage_negative_binary = next(emotion["total_frames"] for emotion in emotions_list_binary if emotion["label"]
                                      == "Negative") / total_frames_binary * 100

    # Determine the final result based on the binary model percentage
    if percentage_negative_binary >= binary_acceptance_threshold:
        # Video is mostly negative
        result_emotions = [emotion for emotion in emotions_list if emotion["label"] in NEGATIVE_EMOTIONS]
        result_emotions_binary = emotions_list_binary
        total_frames = sum([emotion["total_frames"] for emotion in result_emotions_binary])
    else:
        # Translate 7-emotions results to binary results
        result_emotions = emotions_list
        negative_results = reduce_results(result_emotions, NEGATIVE_EMOTIONS)
        positive_results = reduce_results(result_emotions, POSITIVE_EMOTIONS)
        total_frames = sum([emotion["total_frames"] for emotion in result_emotions])

        result_emotions_binary = [
            {"label": "Negative", "total_frames": negative_results["total_frames"], "total_seconds":
                frames_to_seconds(negative_results["total_frames"], fps), "total_sequences":
                negative_results["total_sequences"]},
            {"label": "Positive", "total_frames": positive_results["total_frames"], "total_seconds":
                frames_to_seconds(positive_results["total_frames"], fps), "total_sequences":
                positive_results["total_sequences"]}
        ]

    return result_emotions, result_emotions_binary, total_frames


def calculate_emotion_counts(predictions, class_vocab, frames_amount, fps, video_config):
    emotion_counts = {emotion: {"total_frames": 0, "total_sequences": 0} for emotion in class_vocab}

    # Analyze by sequence
    frames = 0
    for prediction in predictions:
        sequence_results = [np.argmax(result) for result in prediction]
        majority_result = max(set(sequence_results), key=sequence_results.count)
        result_label = class_vocab[majority_result]
        emotion_counts[result_label]["total_sequences"] += 1
        frames += video_config.MAX_SEQ_LENGTH
        if frames >= frames_amount:
            break

    # Analyze by frame
    frames = 0
    for prediction in predictions:
        for result in prediction:
            result_argmax = np.argmax(result)
            result_label = class_vocab[result_argmax]
            # TODO: We should find a better way to avoid the masked results.
            if frames < frames_amount:
                emotion_counts[result_label]["total_frames"] += 1
            frames += 1

    emotions_list = [
        {"label": emotion, "total_frames": counts["total_frames"], "total_seconds":
            frames_to_seconds(counts["total_frames"], fps), "total_sequences": counts["total_sequences"]}
        for emotion, counts in emotion_counts.items()
    ]

    return emotions_list


def reduce_results(results, emotions_included):
    reduced = {'total_frames': 0, 'total_sequences': 0}
    for emotion in results:
        if emotion['label'] in emotions_included:
            reduced['total_frames'] += emotion['total_frames']
            reduced['total_sequences'] += emotion['total_sequences']

    return reduced
