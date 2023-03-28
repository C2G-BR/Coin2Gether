FROM ubuntu:latest

RUN apt-get update -y 
RUN apt-get install -y libpq-dev gcc python3-pip python3-dev 

COPY requirements.txt ./app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "manage.py" ]

# docker build -t server .
# docker run --name server -p 5000:5000 server
# docker tag server bastiberle77/server

# In Case of Errors: docker system prune --all --volumes