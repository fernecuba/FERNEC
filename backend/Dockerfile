FROM python:3.10

COPY ./requirements.txt /requirements.txt

RUN apt-get update && apt-get install -y python3-opencv
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
