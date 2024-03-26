FROM python

COPY xxetester/* /app

RUN pip install lxml \
    && apt-get update \
    && apt-get install -y php8.2 php8.2-cli

WORKDIR /app/target

ENTRYPOINT ["python", "../xxetester.py"] 
