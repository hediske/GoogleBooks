# Stage 1: Build the environment
FROM ubuntu:latest AS build-env
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y wget unzip
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

# Stage 2: Run the app
FROM python:3.11
WORKDIR /app
COPY --from=build-env /app .
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python" , "script.py" ]
