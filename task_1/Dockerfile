FROM python:3.6.6

COPY ./ /tracker
WORKDIR /tracker

ARG POSTGRES_DB
ARG POSTGRES_PASSWORD
ARG POSTGRES_USER
ARG POSTGRES_HOST

ENV POSTGRES_DB=$POSTGRES_DB
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_HOST=$POSTGRES_HOST

RUN pip install -q -r requirements.txt
CMD "chmod +x run.sh"

ENTRYPOINT ["sh", "run.sh"]


