FROM alpine:latest
ENV TINI_URL="https://github.com/krallin/tini/releases/download/v0.18.0/tini-static-amd64"
ENV ALPINE_PACKAGES="python3 py3-pip"

RUN apk --update add ${ALPINE_PACKAGES} \
 && wget -O /tini ${TINI_URL} \
 && chmod +x /tini \
 && mkdir /app

COPY . /app/
WORKDIR /app/

RUN pip3 install -e .

ENTRYPOINT ["/tini", "--"]
CMD ["nutsy"]
