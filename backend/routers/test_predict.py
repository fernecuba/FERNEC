import os
import pytest
from fastapi import BackgroundTasks, HTTPException
from fastapi.testclient import TestClient
from unittest import mock
from starlette.datastructures import FormData

from main import get_app
from .predict import predict_video_endpoint

app, _ = get_app()
client = TestClient(app)


class MockRequest:
    def __init__(self, form_data):
        self._form_data = form_data

    async def form(self):
        return self._form_data


@pytest.mark.asyncio
async def test_predict_video_endpoint_success():
    with mock.patch('backend.routers.predict.predict_video_task') as mock_task:
        mock_task.return_value = None
        form_data = FormData({
            "email": "john.doe@fernec.com",
            "video_file": mock.MagicMock(filename="test_video.mp4", read=mock.AsyncMock(return_value=os.urandom(1024)))
        })


        request = MockRequest(form_data)
        background_tasks = BackgroundTasks()
        assert len(background_tasks.tasks) == 0
        response = await predict_video_endpoint(request, background_tasks)

        assert response.status_code == 202
        assert len(background_tasks.tasks) == 1
        task = background_tasks.tasks[0]
        assert task.func == mock_task
        assert task.args == ("temp_video.mp4", "john.doe@fernec.com", request, background_tasks)


@pytest.mark.asyncio
async def test_predict_video_endpoint_fails():
    with mock.patch('backend.routers.predict.predict_video_task') as mock_task:
        mock_task.return_value = None
        form_data = FormData({
            "email": "john.doe@fernec.com",
            "video_file": mock.MagicMock(filename="test_video.mp4", read=mock.AsyncMock(return_value=os.urandom(1024)))
        })

        request = MockRequest(form_data)
        background_tasks = BackgroundTasks()

        with mock.patch("builtins.open", mock.mock_open()) as mock_file:
            mock_file.side_effect = IOError("fake file write error")
            try:
                response = await predict_video_endpoint(request, background_tasks)
                assert False, "predict_video_endpoint called should have failed"
            except HTTPException as e:
                assert e.status_code == 500
                assert str(e.detail) == "fake file write error"
                assert len(background_tasks.tasks) == 0
