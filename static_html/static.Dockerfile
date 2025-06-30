
FROM python:3.11-slim


WORKDIR /app


# COPY local_file conatiner_destination
COPY ./src .
