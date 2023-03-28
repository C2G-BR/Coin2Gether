# Stage 1
FROM node:19-alpine as build-step
RUN mkdir -p /app
WORKDIR /app
COPY package.json /app
RUN npm install --force
COPY . /app
RUN npm run build --prod --localize

# Stage 2
FROM nginx:1.17.1-alpine
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build-step /app/dist/price-predictor/ /usr/share/nginx/html/

# docker build -t client .
# docker run --name client -p 8888:80 client
# docker tag client bastiberle77/client