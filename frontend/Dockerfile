# pull official base image
FROM node:16.13.0

# install app dependencies
COPY ./package.json ./
COPY ./package-lock.json ./
RUN npm install --silent

COPY ./src ./src
COPY ./public ./public

# start app
CMD ["npm", "start"]