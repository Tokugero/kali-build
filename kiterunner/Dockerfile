FROM golang:1.22.0

COPY kiterunner/ /kiterunner/

WORKDIR /kiterunner

RUN apt-get update && apt-get install -y \
		wget \
		tar && \
	wget https://wordlists-cdn.assetnote.io/data/kiterunner/routes-large.kite.tar.gz && \
	tar -xvf routes-large.kite.tar.gz && \
	make build && \
 	mv dist/kr /usr/local/bin/kr
 
ENTRYPOINT ["/usr/local/bin/kr"]
