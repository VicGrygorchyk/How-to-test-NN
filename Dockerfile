FROM node:16.18.1 as node_build
WORKDIR /project
COPY src/app ./app
RUN cd /project/app && npm i && npm run build


FROM pytorch/pytorch:latest
WORKDIR /app
COPY src/server ./src/server
COPY --from=node_build /project/app/build ./src/server/build
COPY requirements.txt .
COPY tests ./tests
COPY start_server.sh .
RUN apt-get update && apt-get install -y git
RUN pip install -U -r requirements.txt && pip install jupyterlab
EXPOSE 8888 8007
VOLUME models
CMD ["bash", "start_server.sh"]
