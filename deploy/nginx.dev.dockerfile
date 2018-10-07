FROM nginx:1.13.9-alpine
RUN apk add --update --no-cache nginx inotify-tools
COPY deploy/auto-reload-nginx.sh /home/auto.sh
RUN chmod +x /home/auto.sh