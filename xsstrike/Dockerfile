FROM python

COPY ./XSStrike/ /app/

WORKDIR /app/target

RUN pip install -r ../requirements.txt

ENTRYPOINT ["python", "/app/xsstrike.py"]
