FROM python

COPY Flask-Unsign/ /app/

RUN cd /app && \
	pip install .

WORKDIR /app/target

ENTRYPOINT ["flask-unsign"]
