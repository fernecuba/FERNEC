import os
import pytest
from fastapi import BackgroundTasks, HTTPException
from fastapi.testclient import TestClient
from unittest import mock
from starlette.datastructures import FormData

from main import get_app
from .predict import predict_video_endpoint, predict_video_task

app, _ = get_app()
client = TestClient(app)


class PredictVideoEndpointMockRequest:
    def __init__(self, form_data):
        self._form_data = form_data

    async def form(self):
        return self._form_data


@pytest.mark.asyncio
async def test_predict_video_endpoint_success():
    with mock.patch('backend.routers.predict.predict_video_task') as mock_predict_video_task:
        mock_predict_video_task.return_value = None
        form_data = FormData({
            "email": "john.doe@fernec.com",
            "video_file": mock.MagicMock(filename="test_video.mp4", read=mock.AsyncMock(return_value=os.urandom(1024)))
        })


        request = PredictVideoEndpointMockRequest(form_data)
        background_tasks = BackgroundTasks()
        assert len(background_tasks.tasks) == 0
        response = await predict_video_endpoint(request, background_tasks)

        assert response.status_code == 202
        assert len(background_tasks.tasks) == 1
        # task is predict_video_task
        task = background_tasks.tasks[0]
        assert task.func == mock_predict_video_task
        assert task.args == ("temp_video.mp4", "john.doe@fernec.com", request, background_tasks)


@pytest.mark.asyncio
async def test_predict_video_endpoint_fails_with_no_video_file():
    with mock.patch('backend.routers.predict.predict_video_task') as mock_predict_video_task:
        mock_predict_video_task.return_value = None
        form_data = FormData({})

        request = PredictVideoEndpointMockRequest(form_data)
        background_tasks = BackgroundTasks()

        try:
            _ = await predict_video_endpoint(request, background_tasks)
            assert False, "predict_video_endpoint should have failed"
        except HTTPException as e:
            assert e.status_code == 400
            assert str(e.detail) == "Couldn't find video file"
            assert len(background_tasks.tasks) == 0


@pytest.mark.asyncio
async def test_predict_video_endpoint_fails():
    with mock.patch('backend.routers.predict.predict_video_task') as mock_predict_video_task:
        mock_predict_video_task.return_value = None
        form_data = FormData({
            "email": "john.doe@fernec.com",
            "video_file": mock.MagicMock(filename="test_video.mp4", read=mock.AsyncMock(return_value=os.urandom(1024)))
        })

        request = PredictVideoEndpointMockRequest(form_data)
        background_tasks = BackgroundTasks()

        with mock.patch("builtins.open", mock.mock_open()) as mock_file:
            mock_file.side_effect = IOError("fake file write error")
            try:
                _ = await predict_video_endpoint(request, background_tasks)
                assert False, "predict_video_endpoint should have failed"
            except HTTPException as e:
                assert e.status_code == 500
                assert str(e.detail) == "fake file write error"
                assert len(background_tasks.tasks) == 0


class PredictVideoTaskMockRequest:
    class MockApp:
        class MockState:
            def __init__(self):
                self.feature_extractor = mock.MagicMock()
                self.rnn_model = mock.MagicMock()
                self.feature_binary_extractor = mock.MagicMock()
                self.rnn_binary_model = mock.MagicMock()
                self.video_config = mock.MagicMock()

        state = MockState()

    app = MockApp()


@pytest.mark.asyncio
async def test_predict_video_task_success():
    with mock.patch('backend.routers.predict.predict_video') as mock_predict_video, \
            mock.patch('backend.routers.predict.count_frames_per_emotion') as mock_count_frames, \
            mock.patch('backend.routers.predict.send_email_with_prediction_results') as mock_send_email:
        mock_predict_video.return_value = ("prediction_7em", "prediction_binary", 30, 60)
        mock_count_frames.return_value = 1000

        request = PredictVideoTaskMockRequest()
        background_tasks = BackgroundTasks()
        assert len(background_tasks.tasks) == 0
        predict_video_task("temp_video.mp4", "john.doe@fernec.com", request, background_tasks)

        mock_predict_video.assert_called_once()
        mock_count_frames.assert_called_once()
        assert len(background_tasks.tasks) == 1
        # task is send_email_with_prediction_results
        task = background_tasks.tasks[0]
        assert task.func == mock_send_email
        assert task.args == (1000, "john.doe@fernec.com", request)


@pytest.mark.asyncio
async def test_predict_video_task_fails():
    with mock.patch('backend.routers.predict.predict_video') as mock_predict_video, \
            mock.patch('backend.routers.predict.count_frames_per_emotion') as mock_count_frames, \
            mock.patch('backend.routers.predict.send_email_with_prediction_results') as mock_send_email:
        mock_predict_video.side_effect = Exception("Simulated prediction error")

        request = PredictVideoTaskMockRequest()
        background_tasks = BackgroundTasks()

        try:
            predict_video_task("temp_video.mp4", "john.doe@fernec.com", request, background_tasks)
            assert False, "predict_video_task should have failed"
        except Exception:
            mock_predict_video.assert_called_once()
            mock_count_frames.assert_not_called()
            mock_send_email.assert_not_called()
            assert len(background_tasks.tasks) == 0
