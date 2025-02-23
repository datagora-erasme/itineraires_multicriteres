FROM node:iron-alpine3.20

WORKDIR /app

COPY package.json .

RUN npm install

COPY public/ ./public
COPY src/ ./src
COPY tailwind.config.js .

CMD ["npm", "start"]
