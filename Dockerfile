FROM tiangolo/uvicorn-gunicorn:python3.7

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


COPY requirements-app.txt .

RUN pip install -r requirements-app.txt

RUN pyppeteer-install

COPY ./signature_generator /app/signature_generator

COPY ./main.py /app