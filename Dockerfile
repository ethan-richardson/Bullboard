FROM python:3.8.2

# set the home directory to /root \
ENV HOME /root

# cd into the home directory
WORKDIR /root

# Copy all app files into the image
COPY . .

# Allow port 8000 to be accessed
# from outside the container

RUN pip3 install -r requirements.txt

EXPOSE 8000

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

ADD backend/server.py /backend/server.py

CMD /wait && python3 backend/server.py