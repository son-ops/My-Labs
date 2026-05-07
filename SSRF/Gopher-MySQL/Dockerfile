FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        gcc \
        libc6-dev \
        libssl-dev \
        make \
        pkg-config \
        wget \
        zlib1g-dev \
    && wget -q https://curl.se/download/curl-7.61.1.tar.gz \
    && tar -xzf curl-7.61.1.tar.gz \
    && cd curl-7.61.1 \
    && ./configure --with-ssl --disable-shared --enable-static \
    && make -j"$(nproc)" \
    && make install \
    && cd /app \
    && rm -rf curl-7.61.1 curl-7.61.1.tar.gz \
    && apt-get purge -y gcc libc6-dev libssl-dev make pkg-config wget zlib1g-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["sh", "-c", "python init-db.py && python app.py"]
