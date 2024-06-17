FROM golang

COPY ligolo-ng/ /app/

WORKDIR /app/

RUN mkdir /app/target && \
	go build -o agent cmd/agent/main.go && \
	go build -o proxy cmd/proxy/main.go && \
	GOOS=windows go build -o agent.exe cmd/agent/main.go

COPY start.sh /app/start.sh

WORKDIR /app/target

ENTRYPOINT ["/bin/bash", "-c", "/app/start.sh"]
