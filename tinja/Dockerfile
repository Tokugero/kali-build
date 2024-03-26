FROM golang

COPY TInjA/ /app/

RUN cd /app && \
	go install -v github.com/Hackmanit/TInjA@latest

WORKDIR /app/target

ENTRYPOINT ["/go/bin/TInjA"]	
