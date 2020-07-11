FROM alpine:latest

RUN apk add --no-cache python3-dev \
    && apk add --no-cache py-pip

WORKDIR /app

COPY . /app

RUN pip3 --no-cache install Flask \ 
    && pip3 --no-cache-dir install -r requirements.txt \
    && pip3 --no-cache install flask_sqlalchemy 


EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["app.py"]