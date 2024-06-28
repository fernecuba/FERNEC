from .results_consolidation import consolidate_emotion_counts


def test_consolidate_emotion_counts_diff_zero():
    predictions = [{'label': 'Negative', 'total_frames': 278, 'total_seconds': 9, 'total_sequences': 29},
                   {'label': 'Positive', 'total_frames': 52, 'total_seconds': 1, 'total_sequences': 4}]
    total_seconds = 10
    result = consolidate_emotion_counts(predictions, total_seconds)
    assert result == predictions


def test_consolidate_emotion_counts_diff_positive():
    predictions = [{'label': 'Negative', 'total_frames': 278, 'total_seconds': 9, 'total_sequences': 29},
                   {'label': 'Positive', 'total_frames': 52, 'total_seconds': 1, 'total_sequences': 4}]
    total_seconds = 12
    result = consolidate_emotion_counts(predictions, total_seconds)
    expected = [{'label': 'Negative', 'total_frames': 278, 'total_seconds': 11, 'total_sequences': 29},
                {'label': 'Positive', 'total_frames': 52, 'total_seconds': 1, 'total_sequences': 4}]
    assert result == expected


def test_consolidate_emotion_counts_diff_negative():
    predictions = [{'label': 'Negative', 'total_frames': 278, 'total_seconds': 9, 'total_sequences': 29},
                   {'label': 'Positive', 'total_frames': 52, 'total_seconds': 1, 'total_sequences': 4}]
    total_seconds = 8
    result = consolidate_emotion_counts(predictions, total_seconds)
    expected = [{'label': 'Negative', 'total_frames': 278, 'total_seconds': 9, 'total_sequences': 29},
                {'label': 'Positive', 'total_frames': 52, 'total_seconds': 0, 'total_sequences': 4}]
    assert result == expected
