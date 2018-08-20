FROM debian:buster
COPY riscv64-linux-gnu.conf /etc/ld.so.conf.d/
RUN dpkg --add-architecture riscv64 \
 && apt-get update \
 && apt-get install --yes gcc-riscv64-linux-gnu make xxd \
 && ln -s /usr/riscv64-linux-gnu/lib/ld-linux/riscv64-lp64d.so.1 /lib
WORKDIR /src
COPY ./src/ ./
VOLUME /out
ENTRYPOINT ["make"]
