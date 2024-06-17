FROM golang

COPY socialhunter/ /app

WORKDIR /app/target

RUN cd /app && \
	go build . && \
	cp socialhunter /usr/local/bin

ENTRYPOINT ["/usr/local/bin/socialhunter"]
