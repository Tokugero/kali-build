FROM python

RUN mkdir /app

COPY nyxelf/ /app

RUN pip install -r /app/requirements.txt && \
    apt update && \
    apt install -y \
        qemu-kvm \
        libvirt-daemon-system \
        libvirt-clients \
        bridge-utils \
        virt-manager \
        e2tools \
	strace

WORKDIR /app

ENTRYPOINT ["python", "nyxelf.py"] 
