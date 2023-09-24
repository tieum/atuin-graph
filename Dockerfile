FROM python:3.11-slim-buster

WORKDIR /atuin-graph

RUN pip install gunicorn

COPY . .
RUN SETUPTOOLS_SCM_PRETEND_VERSION=1.0 pip install .

ENV SCRIPT_NAME=/graph
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:8889" 

EXPOSE 8889

CMD [ "gunicorn", "atuin_graph.web:app"]
