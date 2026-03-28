FROM php:8.4-cli-bookworm

WORKDIR /var/www

RUN apt-get update && apt-get install -y \
    git \
    unzip \
    libzip-dev \
    default-mysql-client \
    && docker-php-ext-install pdo_mysql zip \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN chmod +x /var/www/entrypoint.sh

ENTRYPOINT ["/var/www/entrypoint.sh"]