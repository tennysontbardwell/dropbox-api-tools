FROM debian

env PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code
ADD src/ /code/
ADD requirements.txt /code/
RUN /code/build.sh

CMD python3 main.py
