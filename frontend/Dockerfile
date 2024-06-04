FROM node:lts-alpine3.17

WORKDIR /app

COPY package.json /app/
COPY package-lock.json /app/
RUN npm install

COPY public/ /app/public
COPY src/ /app/src
COPY README.md /app/
COPY tailwind.config.js /app/

CMD ["npm", "start"]