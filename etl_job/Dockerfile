FROM python:3.8-slim
# this is an operating system (debian-slim)
# with python 3.6 installed on top!

WORKDIR /app
#mkdir /app inside the container

COPY requirements.txt /app
#ADD . /app
# just copy / add over all files into the container's app directory

RUN pip install --trusted-host pypi.python.org -r requirements.txt

#CMD ["python", "tweet_collector.py"]
CMD ["python", "etl.py"]
# Dockerfile always ends with one single command