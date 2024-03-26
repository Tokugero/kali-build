FROM rust

COPY mft/ /app/

RUN cd /app/ && \
	cargo install mft

WORKDIR /app/target

ENTRYPOINT ["mft_dump"]
