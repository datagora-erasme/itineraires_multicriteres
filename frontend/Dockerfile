FROM node:20-alpine
WORKDIR /app
COPY ./ /app
RUN npm install
#ENTRYPOINT ["npm", "start"]
ENTRYPOINT ["tail", "-f", "/dev/null"]