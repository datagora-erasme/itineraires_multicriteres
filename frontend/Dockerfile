FROM node:20-alpine
WORKDIR /app
COPY ./package.json /app
COPY ./package-lock.json /app
COPY ./src /app/src
COPY ./public /app/public
RUN npm install
ENTRYPOINT ["npm", "start"]