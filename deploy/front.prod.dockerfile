FROM warning-service/front as jsbuilder
COPY frontend .
RUN npm run-script build

FROM nginx
RUN apt-get update && apt-get install nano

COPY deploy/nginx.conf /etc/nginx/nginx.conf

COPY --from=jsbuilder /app/dist/ /var/www/html
RUN chown nginx:nginx /var/www/html