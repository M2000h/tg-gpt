FROM python:3.9

RUN apt update -y
RUN apt install -y ffmpeg openvpn

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

COPY credentials.txt /etc/openvpn/credentials.txt
RUN chmod 600 /etc/openvpn/credentials.txt

COPY test.ovpn /etc/openvpn/client.conf

COPY . /app
WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

#CMD ["sh", "-c", "openvpn --config /etc/openvpn/client.conf"]
CMD ["sh", "-c", "openvpn --config /etc/openvpn/client.conf --daemon && python main.py"]

#CMD ["python", "main.py"]