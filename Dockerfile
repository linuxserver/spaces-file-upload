FROM python:3.10.7-alpine
LABEL maintainer="TheLamer"

RUN \
 echo "**** Install python deps ****" && \
 pip install --no-cache-dir \
  boto3 && \
 echo "**** cleanup ****" && \
 rm -rf \
        /tmp/*

# copy local files
COPY upload.py /upload.py
