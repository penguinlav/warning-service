FROM node:9.5
RUN npm install -g vue-cli
RUN mkdir /app
COPY ./frontend/package.json /app
WORKDIR /app
RUN npm install

# RUN apt-get update && apt-get install -y openssh-server
# RUN mkdir /var/run/sshd
# RUN echo 'root:what' | chpasswd
# COPY deploy/sshd_config /etc/ssh/sshd_config
# RUN echo 'root:what' | chpasswd
