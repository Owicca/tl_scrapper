FROM python:3

COPY --from=wcsiu/tdlib:1.8-alpine /usr/local/include/td /usr/local/include/td
COPY --from=wcsiu/tdlib:1.8-alpine /usr/local/lib/libtd* /usr/local/lib/
COPY --from=wcsiu/tdlib:1.8-alpine /usr/lib/libssl.a /usr/local/lib/libssl.a
COPY --from=wcsiu/tdlib:1.8-alpine /usr/lib/libcrypto.a /usr/local/lib/libcrypto.a
COPY --from=wcsiu/tdlib:1.8-alpine /lib/libz.a /usr/local/lib/libz.a
COPY ./web/requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

WORKDIR /app
