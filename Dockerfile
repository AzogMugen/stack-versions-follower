# According to https://pythonspeed.com/articles/base-image-python-docker-images/
FROM python:3.8-slim-buster

# Params to override 
# ENV FLASK_DEBUG True
ARG version

# "Hardcoded" params
ENV FLASK_APP="SVT"
ENV PYTHONDONTWRITEBYTECODE 1
#   ^^^ is it really needed ?

# The Dockerfile itself
COPY . /var/www
WORKDIR /var/www
RUN pip install -r requirements.txt
RUN useradd --create-home flaskpy
USER flaskpy

ENTRYPOINT ["python"]
CMD ["./flask_app/app.py"]
