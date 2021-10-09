FROM python:3.9.7
WORKDIR /app
COPY . .
RUN python3 -m pip install -r ./requirements.txt
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install ffmpeg -y
CMD python3 -u ./main.py
