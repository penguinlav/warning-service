FROM python

WORKDIR /app
ADD ./backend/requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install jupyter 

RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo 'root:what' | chpasswd
COPY deploy/sshd_config /etc/ssh/sshd_config
RUN echo 'root:what' | chpasswd

# SSH login fix. Otherwise user is kicked off after login
# RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

# ENV NOTVISIBLE "in users profile"
# RUN echo "export VISIBLE=now" >> /etc/profile



# RUN apt-get install -y openssh-server
# RUN mkdir echo "PermitRootLogin prohibit-password\nPasswordAuthentication yes\nPermitRootLogin yes\n Port 9922" >> /etc/ssh/sshd_config && (echo 000000; echo 000000) | passwd root

# CMD ["/usr/sbin/sshd", "-D"]
