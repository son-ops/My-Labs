FROM php:8.4-apache

RUN apt-get update \
    && apt-get install -y \
        libzip-dev \
        zip \
        unzip \
    && docker-php-ext-install zip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /var/www/html
COPY index.php /var/www/html/index.php
COPY configs/apache-000.conf /etc/apache2/sites-available/000-default.conf
RUN mkdir -p /var/www/html/upload \
    && chown root:www-data /var/www/html \
    && chmod 775 /var/www/html \
    && chown -R www-data:www-data /var/www/html/upload \
    && chmod -R 775 /var/www/html/upload
RUN name=$(tr -dc 'a-zA-Z0-9' </dev/urandom | head -c 8) && echo 'SSS{test_flag}' > /${name}_flag.txt
EXPOSE 80
