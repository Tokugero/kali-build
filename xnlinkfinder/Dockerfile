FROM python

COPY xnLinkFinder/ /app

WORKDIR /app/target

RUN cd /app/ && python setup.py install

ENTRYPOINT ["python", "/app/xnLinkFinder.py"]
