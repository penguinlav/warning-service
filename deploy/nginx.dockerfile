# This image will contain the javascript code as well since it's nginx serving it.
# Using multi-stage docker build for a smaller final image.
FROM node:9.5 AS jsbuilder

COPY ./client /client
WORKDIR /client

RUN npm install
RUN npm run build

# Multi-stage means the build context needs to be the same, that's a bit disappointing (coupling!)...
FROM nginx:1.13.9-alpine
RUN apt-get update && apt-get install nano

COPY deploy/nginx.conf /etc/nginx/nginx.conf

COPY --from=jsbuilder /client/dist/ /var/www/html
# Make sure sourcemaps are not served (but I still want to access them later on to upload them to sentry)
RUN chown nginx:nginx /var/www/html