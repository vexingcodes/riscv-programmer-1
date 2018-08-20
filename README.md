# docker-flask
Very minimal template for running a Flask application through Gunicorn in a Debian-based Docker container.

## Usage

First, build the container.

```
docker build . -t docker-flask
docker run -d -p 80:80 docker-flask
```

Then load `http://localhost/` in your browser. Simple!
