FROM python:3.9

RUN apt update -y
RUN apt install -y ffmpeg openvpn


COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt


COPY . /app
WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD ["python", "main.py"]