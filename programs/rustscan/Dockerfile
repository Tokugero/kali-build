FROM rust:alpine as builder
LABEL maintainer="RustScan <https://github.com/RustScan>"
RUN apk add --no-cache build-base

# Encourage some layer caching here rather then copying entire directory that includes docs to builder container ~CMN
WORKDIR /app/rustscan
COPY RustScan/Cargo.toml RustScan/Cargo.lock ./
COPY RustScan/src/ src/
RUN cargo build --release

FROM alpine:3.17
LABEL author="Hydragyrum <https://github.com/Hydragyrum>"
LABEL author="LeoFVO <https://github.com/LeoFVO>"
RUN addgroup -S rustscan && \
    adduser -S -G rustscan rustscan && \
    ulimit -n 100000 && \
    apk add --no-cache nmap nmap-scripts wget
USER rustscan
COPY --from=builder /app/rustscan/target/release/rustscan /usr/local/bin/rustscan
WORKDIR /app/target
ENTRYPOINT [ "/usr/local/bin/rustscan" ]
