FROM python

COPY Pickora/ /app/

RUN cd /app && \
	python setup.py install

WORKDIR /app/target

ENTRYPOINT ["pickora"]
