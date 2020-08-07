FROM tiangolo/uvicorn-gunicorn:python3.8

RUN apt-get update && apt-get install -y curl

# 2. Install WebKit dependencies
RUN apt-get install -y libwoff1 \
    libopus0 \
    libwebp6 \
    libwebpdemux2 \
    libenchant1c2a \
    libgudev-1.0-0 \
    libsecret-1-0 \
    libhyphen0 \
    libgdk-pixbuf2.0-0 \
    libegl1 \
    libnotify4 \
    libxslt1.1 \
    libevent-2.1-6 \
    libgles2 \
    libgl1 \
    libvpx5

# 3. Install Chromium dependencies

RUN apt-get install -y libnss3 \
    libxss1 \
    libasound2

RUN apt-get install -y unzip xvfb libxi6 libgconf-2-4

RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
RUN echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get -y install google-chrome-stable

RUN wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip

COPY requirements-app.txt .

RUN pip install -r requirements-app.txt

RUN pyppeteer-install

COPY ./app /app
