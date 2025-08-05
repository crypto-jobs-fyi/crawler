FROM python:3.12-slim

RUN apt-get -y update && \
	apt-get -y upgrade && \
	apt-get install -y --no-install-recommends \
	wget \
	gnupg \
	ca-certificates \
	zip \
	unzip && \
	rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# Install chrome broswer
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get -y install google-chrome-stable

ENV DISPLAY=:99

RUN pip install --upgrade pip

# Install chromedriver
RUN wget -N https://chromedriver.storage.googleapis.com/114.0.5735.16/chromedriver_linux64.zip -P ~/
RUN unzip ~/chromedriver_linux64.zip -d ~/
RUN rm ~/chromedriver_linux64.zip
RUN mv -f ~/chromedriver /usr/local/bin/chromedriver
RUN chown root:root /usr/local/bin/chromedriver
RUN chmod 0755 /usr/local/bin/chromedriver

WORKDIR /data
ADD . /data
RUN pip install -r requirements.txt

CMD ["python3", "crawler.py"]