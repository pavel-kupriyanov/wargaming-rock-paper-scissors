FROM node:13.12.0-alpine

WORKDIR /opt/app

ENV REACT_APP_SERVER_URL $REACT_APP_SERVER_URL

COPY ./ .
RUN npm install

CMD ["npm", "start"]
