FROM python:3.6
RUN mkdir -p /opt/kubepy

COPY ./app.py /opt/kubepy/
COPY ./requirements.txt /opt/kubepy/
COPY ./templates /opt/kubepy/templates

RUN pip install -r /opt/kubepy/requirements.txt

USER nobody
WORKDIR /opt/kubepy


ENTRYPOINT ["python3","-u","app.py"]
