FROM alpine:3.4

RUN	apk add --no-cache gcc libc-dev libffi-dev libgit2=0.24.1-r0 libgit2-dev=0.24.1-r0 python3 python3-dev && \
	pip3 install cffi && \
	pip3 install Django==1.10.3 pygit2==0.24.1 && \
	apk del gcc libc-dev libffi-dev libgit2-dev python3-dev

COPY . /usr/share/vanadis/
RUN /usr/share/vanadis/manage.py migrate

EXPOSE 80
CMD /usr/share/vanadis/manage.py runserver 0.0.0.0:80
