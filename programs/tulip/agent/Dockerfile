FROM debian:bookworm-slim

RUN apt-get update && \
    # Install ssh, nc, vim, curl, wget, tcpdump
    apt-get install -y openssh-client netcat-openbsd vim curl wget tcpdump && \
    # Clean apt cache
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /root/.ssh

COPY ./entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]