FROM python:3.9-alpine
RUN mkdir /app
COPY . /app/
WORKDIR /app
RUN python -m venv .venv && \
  .venv/bin/pip install -i https://mirrors.163.com/pypi/simple pipenv && \
  .venv/bin/pipenv install
ENTRYPOINT /bin/sh /app/entrypoint.sh
