from python:3.7-alpine as base-env
RUN apk add --no-cache --virtual .build-deps gcc musl-dev
RUN python3 -m pip install pymongo dnspython

FROM base-env as test-container
COPY ./test.py /test.py

WORKDIR /
CMD [ "python3", "test.py" ]


