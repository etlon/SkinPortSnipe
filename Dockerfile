FROM debian:latest
LABEL authors="Cedric"
FROM python:3.10
WORKDIR /myapp
COPY images /myapp/images
ADD Item.py link.save main.py Methods.py requirements.txt skinportsnipeicon.ico /myapp/

RUN apt-get -y update
RUN pip install --upgrade pip
RUN apt-get install zip -y
RUN apt-get install unzip -y
RUN pip install -r requirements.txt
RUN apt-get install -y locales locales-all

RUN sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen \
&& locale-gen

ENV LANG de_DE.UTF-8
ENV LC_ALL de_DE.UTF-8



# Install chromedriver
RUN wget -N https://chromedriver.storage.googleapis.com/72.0.3626.69/chromedriver_linux64.zip -P ~/
RUN unzip ~/chromedriver_linux64.zip -d ~/
RUN rm ~/chromedriver_linux64.zip
RUN mv -f ~/chromedriver /usr/local/bin/chromedriver
RUN chown root:root /usr/local/bin/chromedriver
RUN chmod 0755 /usr/local/bin/chromedriver


# Install chrome broswer
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get -y install google-chrome-stable

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

#RUN mkdir images
#COPY ./images srv/images/
#ADD main.py Item.py Methods.py link.save skinportsnipeicon.ico ./

EXPOSE 8686:8080

CMD ["python", "-u", "main.py"]
