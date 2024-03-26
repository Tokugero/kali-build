FROM python:2.7-stretch

COPY tplmap/ /app/

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "tplmap.py"]

