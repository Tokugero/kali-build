FROM python

COPY python-uncompyle6/ /app/

WORKDIR /app/target

RUN pip install -e ..

ENTRYPOINT ["uncompyle6"]
