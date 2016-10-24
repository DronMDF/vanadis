FROM ubuntu:16.10
ENV DEBIAN_FRONTEND noninteractive
ENV LAST_UPDATED 2013-12-20
ENV TERM linux
RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y python3-django
RUN apt-get install -y python3-pygit2
RUN apt-get clean -y
RUN apt-get autoremove -y
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
COPY . /usr/share/vanadis/
RUN /usr/share/vanadis/manage.py migrate
EXPOSE 80
CMD /usr/share/vanadis/manage.py runserver 0.0.0.0:80
