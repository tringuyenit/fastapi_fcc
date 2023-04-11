FROM nginx:1.15.8-alpine

#config
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/nginx.conf
RUN apk update && apk add bash