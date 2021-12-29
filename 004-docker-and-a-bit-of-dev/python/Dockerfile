FROM python:3.9-alpine
# additional args for pip command, like -i http://pypi-mirror/...
ARG PIPARG ""
RUN mkdir /app
COPY . /app/
WORKDIR /app
RUN python -m venv .venv && \
  .venv/bin/pip install $PIPARG pipenv && \
  .venv/bin/pipenv install
ENTRYPOINT /bin/sh /app/entrypoint.sh
