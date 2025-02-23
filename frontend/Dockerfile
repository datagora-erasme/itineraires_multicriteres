FROM node:iron-alpine3.20

WORKDIR /app

COPY package-lock.json /app/
COPY package.json /app/
RUN npm install

COPY public/ /app/public
COPY src/ /app/src
COPY tailwind.config.js /app/

CMD ["npm", "start"]