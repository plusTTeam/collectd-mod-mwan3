FROM alpine:latest
RUN apk update && apk add collectd
RUN apk add python2 && apk add collectd-python
COPY collectd.conf /etc/collectd/collectd.conf
CMD tail -f /dev/null