FROM gliderlabs/python-runtime:3.4

MAINTAINER matlockx@sounds.so

EXPOSE 8080
ENV PYTHONUNBUFFERED=1

CMD ["/env/bin/python", "-m", "bottle", "-s", "cherrypy", "-b", "0.0.0.0:8080", "--debug", "main"]
