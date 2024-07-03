import pytest
from unittest import mock

from .video_predictor import count_frames_per_emotion
from .models import VideoConfig


@pytest.fixture
def mock_listdir():
    with mock.patch('backend.routers.video_predictor.os.listdir',
                    return_value=['frame1.jpg', 'frame2.jpg', 'frame3.jpg']) as frames_mocked:
        yield frames_mocked


@pytest.fixture
def mock_consolidate_results():
    with mock.patch('backend.routers.results_consolidation.consolidate_results') as results_mocked:
        results_mocked.return_value = (
            [
                {"label": "Neutral", "total_frames": 2, "total_seconds": 0.07},
                {"label": "Anger", "total_frames": 1, "total_seconds": 0.03}
            ],
            [
                {"label": "Negative", "total_frames": 2, "total_seconds": 0.07},
                {"label": "Positive", "total_frames": 1, "total_seconds": 0.03}
            ],
            3
        )
        yield results_mocked


@pytest.fixture
def mock_video_config():
    return VideoConfig(
        MAX_SEQ_LENGTH=2,
        FRAMES_ORDER_MAGNITUDE=5,
        HEIGHT=112,
        WIDTH=112,
        CHANNELS=3,
        NUM_FEATURES=1024,
        FACE_BATCH_SIZE=500
    )


# TODO: this test should be improved to be more accurate
@pytest.mark.asyncio
async def test_count_frames_per_emotion_success(mock_listdir, mock_consolidate_results, mock_video_config):
    predictions = [
        [0.1, 0.9], [0.2, 0.8], [0.3, 0.7]
    ]
    predictions_binary = [
        [0.1, 0.9], [0.2, 0.8], [0.3, 0.7]
    ]
    fps = 30
    duration = 3

    result = count_frames_per_emotion(predictions, predictions_binary, fps, duration, mock_video_config)

    expected_result = {
        "total_frames": 3,
        "real_total_seconds": 3,
        "total_seconds": 0,
        "fps": 30,
        "emotions": [
            {"label": "Anger", "total_frames": 0, "total_seconds": 0, "total_sequences": 0},
            {"label": "Disgust", "total_frames": 0, "total_seconds": 0, "total_sequences": 0},
            {"label": "Fear", "total_frames": 0, "total_seconds": 0, "total_sequences": 0},
            {"label": "Sadness", "total_frames": 0, "total_seconds": 0, "total_sequences": 0},
            {"label": "Surprise", "total_frames": 0, "total_seconds": 0, "total_sequences": 0},
            {"label": "Neutral", "total_frames": 0, "total_sequences": 0, "total_seconds": 0},
            {"label": "Happiness", "total_frames": 0, "total_sequences": 0, "total_seconds": 0}
        ],
        "emotions_binary": [
            {"label": "Negative", "total_frames": 3, "total_seconds": 0, "total_sequences": 2},
            {"label": "Positive", "total_frames": 0, "total_seconds": 0, "total_sequences": 0}
        ],
    }
    print(f"result is {result}")
    mock_consolidate_results.assert_called_once()
    assert result == expected_result
