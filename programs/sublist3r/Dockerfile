FROM python

COPY Sublist3r/ /app

WORKDIR /app/target

RUN pip install -r /app/requirements.txt

ENTRYPOINT ["python", "/app/sublist3r.py"]
