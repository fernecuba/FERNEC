FROM python:3.10

COPY ./requirements.txt /requirements.txt
COPY ./preprocessing/frames_generator/requirements.txt /preprocessing/frames_generator/requirements.txt

RUN apt-get update && apt-get install -y python3-opencv ffmpeg
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
RUN pip install --no-cache-dir -r /preprocessing/frames_generator/requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
