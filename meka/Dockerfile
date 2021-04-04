FROM ubuntu

RUN apt update
RUN apt install python3-dev

RUN pip install -r requirements.txt

COPY . /opt/meka

ENTRYPOINT ["python run.py"]