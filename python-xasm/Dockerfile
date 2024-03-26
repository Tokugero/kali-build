FROM python

COPY python-xasm/ /app/python-xasm/
COPY python-xdis/ /app/python-xdis/

WORKDIR /app/target

RUN pip install -e ../python-xasm/ && \
	pip install -e ../python-xdis/

