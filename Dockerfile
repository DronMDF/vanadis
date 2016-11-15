FROM dronmdf/vanadis:base
COPY . /usr/share/vanadis/
RUN /usr/share/vanadis/manage.py migrate
EXPOSE 80
CMD /usr/share/vanadis/manage.py runserver 0.0.0.0:80
