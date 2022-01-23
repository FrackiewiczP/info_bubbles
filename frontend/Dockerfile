FROM node:16.13.0

# install serve tool for serving the site
RUN npm install -g serve

# install app dependencies
COPY ./package.json ./
COPY ./package-lock.json ./
RUN npm install --silent

# copy source code
COPY ./src ./src
COPY ./public ./public

# create production build
RUN npm run build

# start the app
CMD ["serve", "-s", "build"]
