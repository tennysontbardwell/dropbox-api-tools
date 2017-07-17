FROM debian

env PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code

ADD dependencies/ /code/
RUN /code/build-dependencies.sh

ADD src/ /code/
RUN /code/build.sh

CMD python3 main.py
